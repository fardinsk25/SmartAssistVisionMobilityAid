import cv2
import numpy as np

# MobileNetSSD class labels
CLASSES = [
    "background", "aeroplane", "bicycle", "bird", "boat",
    "bottle", "bus", "car", "cat", "chair", "cow",
    "diningtable", "dog", "horse", "motorbike", "person",
    "pottedplant", "sheep", "sofa", "train", "tvmonitor"
]

# Load MobileNetSSD model
net = cv2.dnn.readNetFromCaffe(
    "models/MobileNetSSD_deploy.prototxt",
    "models/MobileNetSSD_deploy.caffemodel"
)

# Open webcam
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()

    if not ret:
        print("Camera not detected!")
        break

    (h, w) = frame.shape[:2]

    # Create blob
    blob = cv2.dnn.blobFromImage(
        cv2.resize(frame, (300, 300)),
        scalefactor=0.007843,
        size=(300, 300),
        mean=127.5
    )

    # Run detection
    net.setInput(blob)
    detections = net.forward()

    # Draw guide lines for Left-Center-Right
    cv2.line(frame, (w // 3, 0), (w // 3, h), (255, 0, 0), 2)
    cv2.line(frame, (2 * w // 3, 0), (2 * w // 3, h), (255, 0, 0), 2)

    for i in range(detections.shape[2]):

        confidence = detections[0, 0, i, 2]

        if confidence > 0.5:

            idx = int(detections[0, 0, i, 1])

            box = detections[0, 0, i, 3:7] * np.array(
                [w, h, w, h]
            )

            (startX, startY, endX, endY) = box.astype("int")

            # Get object name
            label = CLASSES[idx]

            # Find object center
            center_x = (startX + endX) // 2

            # Determine position
            if center_x < w // 3:
                position = "Left"
            elif center_x < 2 * w // 3:
                position = "Center"
            else:
                position = "Right"

            # Display text
            text = f"{label} - {position}"

            # Draw bounding box
            cv2.rectangle(
                frame,
                (startX, startY),
                (endX, endY),
                (0, 255, 0),
                2
            )

            # Draw object label
            cv2.putText(
                frame,
                text,
                (startX, startY - 10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                (0, 255, 0),
                2
            )

    cv2.imshow("Smart Vision - Object Detection", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()