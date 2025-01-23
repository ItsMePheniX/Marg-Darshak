# Code for object detection and guidance system
import cv2
from ultralytics import YOLO
import pyttsx3
import threading

# Initialize the YOLOv8 model
model = YOLO('yolov8n.pt')

# Initialize text-to-speech engine
tts_engine = pyttsx3.init()
tts_engine.setProperty('rate', 150)
tts_engine.setProperty('volume', 0.9)

# List of objects to announce and their real-world heights (in meters)
objects_to_announce = {
    'car': 1.5,
    'bus': 3.0,
    'person': 1.7,
    'stairs': 0.2,
    'pothole': 0.1,
    'speed bump': 0.15,
    'cell phone': 0.16 
}

# Focal length
FOCAL_LENGTH = 220

# Define the video stream from the Raspberry Pi camera feed
feed_laptopIP = "http://192.168.137.237:5000//video_feed"
cap = cv2.VideoCapture(feed_laptopIP)

if not cap.isOpened():
    print("Error: Could not open video stream")
    exit()

# Function to announce detected objects asynchronously
def announce_object(message):
    tts_thread = threading.Thread(target=speak, args=(message,))
    tts_thread.start()

# Function to speak the message
def speak(message):
    tts_engine.say(message)
    tts_engine.runAndWait()

# Real-time object detection loop
while True:
    ret, frame = cap.read()
    if not ret:
        print("Failed to capture frame")
        break

    # Run YOLOv8 detection on the frame
    results = model(frame)
    frame_height, frame_width, _ = frame.shape

    # Path zone: Only objects within this central region are considered
    path_left = frame_width / 3
    path_right = 2 * frame_width / 3

    # Process detection results
    for result in results:
        for obj in result.boxes:
            class_id = int(obj.cls)
            object_name = model.names[class_id]
            confidence = obj.conf.item()
            box = obj.xyxy[0]  # Bounding box coordinates (x1, y1, x2, y2)

            if object_name in objects_to_announce and confidence > 0.5:
                # Calculate object position and size
                x1, y1, x2, y2 = box
                center_x = (x1 + x2) / 2
                box_height = max(y2 - y1, 1)  # Avoid division by zero

                # Estimate distance
                real_height = objects_to_announce[object_name]
                distance = (FOCAL_LENGTH * real_height) / box_height
                distance = round(float(distance), 2)#Change for accuracy
            
                # Debugging print
                print(f"Object: {object_name}, Box Height (pixels): {box_height}, Estimated Distance: {distance} meters")

                # Determine direction only if in path zone
                if path_left <= center_x <= path_right:
                    if center_x < frame_width / 2:
                        direction = "Move slightly to your right"
                    else:
                        direction = "Move slightly to your left"
                    
                    # Prepare and announce the guidance message
                    message = f"{object_name} detected at {distance} meters. {direction}."
                    announce_object(message)

    # Visualize results
    annotated_frame = results[0].plot()
    cv2.imshow('Navigation Assist', annotated_frame)

    if cv2.waitKey(1) & 0xFF == ord('f'):
        break

cap.release()
cv2.destroyAllWindows()