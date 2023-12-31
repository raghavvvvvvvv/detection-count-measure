from ultralytics import YOLO
import cv2
import cvzone
import math
import time

# Define the known distance between two points in the scene
KNOWN_DISTANCE = 100  # in centimeters

cap = cv2.VideoCapture(0)  # For Webcam
cap.set(3, 1280)
cap.set(4, 720)

model = YOLO('../yolo_weights/yolov8n.pt')

classNames = ["person", "bicycle", "car", "motorbike", "aeroplane", "bus", "train", "truck", "boat",
              "traffic light", "fire hydrant", "stop sign", "parking meter", "bench", "bird", "cat",
              "dog", "horse", "sheep", "cow", "elephant", "bear", "zebra", "giraffe", "backpack", "umbrella",
              "handbag", "tie", "suitcase", "frisbee", "skis", "snowboard", "sports ball", "kite", "baseball bat",
              "baseball glove", "skateboard", "surfboard", "tennis racket", "bottle", "wine glass", "cup",
              "fork", "knife", "spoon", "bowl", "banana", "apple", "sandwich", "orange", "broccoli",
              "carrot", "hot dog", "pizza", "donut", "cake", "chair", "sofa", "pottedplant", "bed",
              "diningtable", "toilet", "tvmonitor", "laptop", "mouse", "remote", "keyboard", "cell phone",
              "microwave", "oven", "toaster", "sink", "refrigerator", "book", "clock", "vase", "scissors",
              "teddy bear", "hair drier", "toothbrush"
              ]

prev_frame_time = 0
new_frame_time = 0
while True:
    new_frame_time = time.time()
    success, img = cap.read()
    results = model(img, stream=True)
    person_count = 0
    for r in results:
        boxes = r.boxes
        for box in boxes:
            cls = int(box.cls[0])
            if cls == 0:  # if class is "person"
                person_count += 1
                # Bounding Box
                x1, y1, x2, y2 = box.xyxy[0]
                x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
                w, h = x2 - x1, y2 - y1
                cvzone.cornerRect(img, (x1, y1, w, h))
                # Confidence
                # conf = math.ceil((box.conf[0] * 100)) / 100
                cvzone.putTextRect(img, f'{classNames[cls]}', (max(0, x1), max(35, y1)), scale=2, thickness=2)

                # Calculate Distance
                person_height = 2.7  # average height of a person in meters
                focal_length = 875  # focal length of the camera lens (change this according to your camera)
                distance = (focal_length * person_height) / h
                cv2.putText(img, f"Distance: {round(distance, 2)} ft", (x1, y1 - 35), cv2.FONT_HERSHEY_SIMPLEX, 1,
                            (255, 0, 0), 2)

    cv2.putText(img, f'Total Persons : {person_count}', (40, 70), cv2.FONT_HERSHEY_DUPLEX, 0.8, (255, 0, 0), 2)
    fps = 1 / (new_frame_time - prev_frame_time)
    prev_frame_time = new_frame_time
    print(fps)

    cv2.imshow("Image", img)

    # Check for "ESC" key press
    key = cv2.waitKey(1)
    if key == 27:  # "ESC" key
        break

# Release the resources and close the window
cap.release()
cv2.destroyAllWindows()