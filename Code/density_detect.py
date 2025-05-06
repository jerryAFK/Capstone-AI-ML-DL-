# detect_density.py
from ultralytics import YOLO
import cv2
import numpy as np

# Load models
model_ambulance = YOLO(r'D:\Class\Capstone\FY-CSE-CAP\Code\myDetectionModel\yolo8l_allvehicles2\weights\best.pt')  # Your ambulance model
model_general = YOLO('yolov8l.pt')  # Pretrained for general vehicles

# List of classes to count
vehicle_classes = ['car', 'truck', 'bus', 'motorcycle']

# Function to detect vehicles and ambulances
def detect_vehicles_and_ambulance(image_path):
    img = cv2.imread(image_path)

    img_height, img_width, _ = img.shape

    # Define lane boundaries (simple division into 3 vertical strips)
    lane1 = (0, img_width // 3)
    lane2 = (img_width // 3, 2 * img_width // 3)
    lane3 = (2 * img_width // 3, img_width)

    lanes = {'left': 0, 'center': 0, 'right': 0}

    ambulance_detected = False

    # Detect ambulances
    results_ambulance = model_ambulance(img, conf=0.2)

    for r in results_ambulance:
        for box in r.boxes:
            label = model_ambulance.names[int(box.cls[0])]
            if label.lower() == 'ambulance':
                ambulance_detected = True
    
    # Detect general vehicles
    results_general = model_general(img, conf=0.2)

    for r in results_general:
        for box in r.boxes:
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            label = model_general.names[int(box.cls[0])]
            
            if label in vehicle_classes:
                # Find center of bounding box
                center_x = (x1 + x2) // 2

                # Decide which lane it belongs to
                if lane1[0] <= center_x < lane1[1]:
                    lanes['left'] += 1
                elif lane2[0] <= center_x < lane2[1]:
                    lanes['center'] += 1
                elif lane3[0] <= center_x < lane3[1]:
                    lanes['right'] += 1


    # Final output
    output = {
        'lanes': lanes,
        'ambulance_detected': ambulance_detected
    }

    return output

# Quick test
if __name__ == "__main__":
    image_path = r"D:\Class\Capstone\FY-CSE-CAP\Code\input Images\Screenshot 2025-04-06 205827.png"
    result = detect_vehicles_and_ambulance(image_path)
    print(result)
