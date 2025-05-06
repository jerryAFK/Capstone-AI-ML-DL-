from ultralytics import YOLO
import cv2
import os

# Load models
model_general = YOLO("yolov8l.pt")  # Pretrained YOLO for general vehicles
model_ambulance = YOLO(r"D:\Class\Capstone\FY-CSE-CAP\Code\myDetectionModel\yolo8l_allvehicles2\weights\best.pt")  # Your ambulance model

# Define paths
inputPath = os.getcwd() + "/Images/"
outputPath = os.getcwd() + "/output_images/"

# Function to detect vehicles
def detectVehicles(filename):
    global model_general, model_ambulance, inputPath, outputPath
    img = cv2.imread(inputPath + filename)

    # Perform detections
    results_ambulance = model_ambulance(img, conf=0.2)
    results_general = model_general(img, conf=0.2)
    
    # Draw ambulance detections
    for r in results_ambulance:
        for box in r.boxes:
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            label = model_ambulance.names[int(box.cls[0])]

            if label.lower() == "ambulance":
                box_color = (0, 0, 255)  # Red for ambulances
                label_bg_color = (255, 255, 255)
                font_color = (0, 0, 0)

                (text_width, text_height), _ = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 1)
                label_bg_start = (x1, y1 - text_height - 5)
                label_bg_end = (x1 + text_width, y1)

                img = cv2.rectangle(img, (x1, y1), (x2, y2), box_color, 2)
                img = cv2.rectangle(img, label_bg_start, label_bg_end, label_bg_color, -1)
                img = cv2.putText(img, label, (x1, y1 - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, font_color, 1)

    # Draw general vehicle detections
    for r in results_general:
        for box in r.boxes:
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            label = model_general.names[int(box.cls[0])]

            if label in ["car", "truck", "bus", "motorcycle"]:
                box_color = (0, 255, 0)  # Green for normal vehicles
                label_bg_color = (255, 255, 255)
                font_color = (0, 0, 0)

                (text_width, text_height), _ = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 1)
                label_bg_start = (x1, y1 - text_height - 5)
                label_bg_end = (x1 + text_width, y1)

                img = cv2.rectangle(img, (x1, y1), (x2, y2), box_color, 2)
                img = cv2.rectangle(img, label_bg_start, label_bg_end, label_bg_color, -1)
                img = cv2.putText(img, label, (x1, y1 - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, font_color, 1)


    outputFilename = outputPath + "output_" + filename
    cv2.imwrite(outputFilename, img)
    print('Output image stored at:', outputFilename)

# Run detection on all images
for filename in os.listdir(inputPath):
    if filename.endswith((".png", ".jpg", ".jpeg")):
        detectVehicles(filename)

print("✅ Done!")
