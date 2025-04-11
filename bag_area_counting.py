from ultralytics import YOLO
import cv2
import os
from save_to_db import save_detected_product
import json

# Load the model
model = YOLO('pos.pt')

# Open webcam
cap = cv2.VideoCapture(0)

# Load or define ROI (region of interest)
roi_file = "roi.txt"
if os.path.exists(roi_file):
    with open(roi_file, 'r') as file:
        r = tuple(map(int, file.readline().split(',')))
else:
    success, img = cap.read()
    if not success:
        print("Error: Failed to read frame")
        cap.release()
        cv2.destroyAllWindows()
        exit()
    cv2.namedWindow("Select the area")
    r = cv2.selectROI("Select the area", img, fromCenter=False, showCrosshair=True)
    cv2.destroyWindow("Select the area")
    with open(roi_file, 'w') as file:
        file.write(','.join(map(str, r)))

zone_left, zone_top, zone_width, zone_height = r
zone_right = zone_left + zone_width
zone_bottom = zone_top + zone_height

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

    cv2.imshow("Bagging Area", frame)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
