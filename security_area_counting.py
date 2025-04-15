from ultralytics import YOLO
import cv2
import os
from save_to_db_security import save_detected_product
import json
import pyautogui
import sys
import pygetwindow as gw
from screeninfo import get_monitors
import time

base_dir = os.path.dirname(os.path.abspath(__file__))

model_path = os.path.join(base_dir, "pos.pt")

# Load the model
model = YOLO(model_path)
# Open webcam
cap = cv2.VideoCapture(1)
cap.set(3, 640)  # Width
cap.set(4, 480) 


def move_cv2_window_to_third_screen(window_title):
    time.sleep(2)  # Let the window appear first
    try:
        win = gw.getWindowsWithTitle(window_title)[0]
        screens = get_monitors()

        if len(screens) >= 3:
            screen3 = screens[2]
            screen3_width = screen3.width
            screen3_height = screen3.height

            # Position to LEFT HALF of third screen
            new_x = screen3.x
            new_y = screen3.y
            new_width = screen3_width // 2
            new_height = screen3_height  # or set a fixed height if needed

            win.moveTo(new_x, new_y)
            win.resizeTo(new_width, new_height)
            print(f"✅ OpenCV window moved to left half of 3rd screen at ({new_x}, {new_y}), size ({new_width}x{new_height})")
        else:
            print("⚠️ Less than 3 monitors detected.")
    except Exception as e:
        print("❌ Error moving OpenCV window:", e)



# Get window screen width, height
screen_width , screen_height = pyautogui.size()

video_width = screen_width //2
aspect_ratio = 640/480
# video_height = int(video_width/aspect_ratio)
video_height = 700

# Load or define ROI (region of interest)
roi_file = os.path.join(base_dir,"security_area_roi.txt")
if os.path.exists(roi_file):
    with open(roi_file, 'r') as file:
        r = tuple(map(int, file.readline().split(',')))
else:
    success, img = cap.read()
    if not success:
        print("Error: Failed to read frame")
        cap.release()
        cv2.destroyAllWindows()
        sys.exit()
    cv2.namedWindow("Select the area")
    r = cv2.selectROI("Select the area", img, fromCenter=False, showCrosshair=True)
    cv2.destroyWindow("Select the area")
    with open(roi_file, 'w') as file:
        file.write(','.join(map(str, r)))

zone_left, zone_top, zone_width, zone_height = r
zone_right = zone_left + zone_width
zone_bottom = zone_top + zone_height
cv2.namedWindow("Bagging Area", cv2.WINDOW_NORMAL)
cv2.namedWindow("Bagging Area", cv2.WND_PROP_FULLSCREEN)
cv2.setWindowProperty("Bagging Area", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
cv2.moveWindow("Bagging Area", 0, 0)    
#cv2.resizeWindow("Bagging Area", video_width, video_height) 
moved = False
while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Run detection only (not tracking)
    results = model(frame, conf=0.5, iou=0.5)[0]

    # Count items currently inside ROI in this frame
    current_count = 0

    if results.boxes is not None:
        for i, box in enumerate(results.boxes.xyxy):
          
            x1, y1, x2, y2 = map(int, box.tolist())
            cx, cy = (x1 + x2) // 2, (y1 + y2) // 2

            # Only count objects inside the ROI
            if zone_left < cx < zone_right and zone_top < cy < zone_bottom:
                current_count += 1
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)

    # Draw the ROI
    cv2.rectangle(frame, (zone_left, zone_top), (zone_right, zone_bottom), (0, 0, 255), 2)
    cv2.putText(frame, "Bagging Area", (zone_left + 10, zone_top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

    # Display count on frame
    cv2.putText(frame, f"Total count {current_count}", (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)
    json_txt = json.dumps(current_count)
    save_detected_product(json_txt)

    if not moved:
        move_cv2_window_to_third_screen("Bagging Area")
        moved = True  
    cv2.imshow("Bagging Area", frame)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
