from ultralytics import YOLO
import cv2

# Load lightweight model
model = YOLO("yolov8n.pt")

def process_frame(frame):
    """
    Process a frame:
    - Resize for speed
    - Detect people
    - Draw bounding boxes
    - Return frame + count
    """

    # Resize (major speed improvement)
    frame = cv2.resize(frame, (640, 360))

    # Run detection with smaller image size
    results = model(frame, imgsz=320, conf=0.3)[0]

    count = 0

    for box in results.boxes:
        cls = int(box.cls[0])

        if cls == 0:  # person
            count += 1

            x1, y1, x2, y2 = map(int, box.xyxy[0])

            # Draw bounding box
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)

    return frame, count