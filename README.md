
# POS_Counting_system

Nowadays, retail is moving towards Artificial Intelligence. So in this project, I have created an AI-based real-time product counting system built using the Ultralytics YOLO object detection model and OpenCV.

It uses a connected webcam to:

Detect and count products placed on the bagging area or table.

Display the total number of items present in real-time.

Save the total counts in a JSON file, which can be stored in a database for further use.

This system works even if new products are introduced, as long as the model detects them—it will include them in the count.




## 🔧 Features

📷 Live video stream from webcam

📦 Detects objects using a trained YOLO model

📍 Selectable Region of Interest (ROI) for focused detection

🔢 Displays total number of products currently visible in the frame

📝 Saves total count to a JSON file

⚙️ Adjustable confidence and IOU thresholds
## Getting started
1. Clone this Repository

## Run Locally

Clone the project

```bash
  git clone https://github.com/Amalaseeli/POS_Counting_system.git
```

Go to the project directory

```bash
  cd POS_Counting_system
```

Install dependencies

```bash
  pip install -r requirements.txt
```



## Run the project
``` bash
python bag_area_counting.py
```
