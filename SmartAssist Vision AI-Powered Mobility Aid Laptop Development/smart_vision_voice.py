import cv2
import numpy as np
import pyttsx3
import threading
import time

# MobileNetSSD classes
CLASSES = [
    "background", "aeroplane", "bicycle", "bird", "boat",
    "bottle", "bus", "car", "cat", "chair", "cow",
    "diningtable", "dog", "horse", "motorbike", "person",
    "pottedplant", "sheep", "sofa", "train", "tvmonitor"
]

# Load model
net = cv2.dnn.readNetFromCaffe(
    "models/MobileNetSSD_deploy.prototxt",
    "models/MobileNetSSD_deploy.caffemodel"
)

# Voice engine
engine = pyttsx3.init()
engine.setProperty('rate', 150)

# Global variables
last_spoken = ""
last_time = 0
speech_busy = False


def speak(text):
    global speech_busy

    speech_busy = True

    engine.say(text)
    engine.runAndWait()

    speech_busy = False


# Open webcam
cap = cv2.VideoCapture(0)

while True:

    ret, frame = cap.read()

    if not ret:
        print("Camera not found")
        break

    (h, w) = frame.shape[:2]

    # Left-Center-Right guide lines
    cv2.line(frame, (w // 3, 0), (w // 3, h), (255, 0, 0), 2)
    cv2.line(frame, (2 * w // 3, 0), (2 * w // 3, h), (255, 0, 0), 2)

    blob = cv2.dnn.blobFromImage(
        cv2.resize(frame, (300, 300)),
        0.007843,
        (300, 300),
        127.5
    )

    net.setInput(blob)
    detections = net.forward()

    current_message = ""

    # Find best detection
    best_area = 0

    for i in range(detections.shape[2]):

        confidence = detections[0, 0, i, 2]

        if confidence > 0.6:

            idx = int(detections[0, 0, i, 1])

            box = detections[0, 0, i, 3:7] * np.array(
                [w, h, w, h]
            )

            (startX, startY, endX, endY) = box.astype("int")

            area = (endX - startX) * (endY - startY)

            if area > best_area:

                best_area = area

                label = CLASSES[idx]

                center_x = (startX + endX) // 2

                if center_x < w // 3:
                    position = "left"
                elif center_x < 2 * w // 3:
                    position = "center"
                else:
                    position = "right"

                current_message = f"{label} on the {position}"

                best_box = (startX, startY, endX, endY)

    # Draw only the largest object
    if current_message != "":

        startX, startY, endX, endY = best_box

        cv2.rectangle(
            frame,
            (startX, startY),
            (endX, endY),
            (0, 255, 0),
            2
        )

        cv2.putText(
            frame,
            current_message,
            (startX, startY - 10),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (0, 255, 0),
            2
        )

        now = time.time()

        # Speak when position/object changes
        if current_message != last_spoken:

            print("Speaking:", current_message)

            threading.Thread(
                target=speak,
                args=(current_message,),
                daemon=True
            ).start()

            last_spoken = current_message
            last_time = now

        # Repeat every 3 seconds
        elif now - last_time > 3 and not speech_busy:

            print("Repeating:", current_message)

            threading.Thread(
                target=speak,
                args=(current_message,),
                daemon=True
            ).start()

            last_time = now

    cv2.imshow("Smart Vision Assistant", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()