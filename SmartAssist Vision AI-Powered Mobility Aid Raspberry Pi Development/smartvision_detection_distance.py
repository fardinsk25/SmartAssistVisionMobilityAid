import cv2
import numpy as np
import RPi.GPIO as GPIO
import time

# ==========================
# HC-SR04 SETUP
# ==========================

TRIG = 23
ECHO = 24

GPIO.setmode(GPIO.BCM)
GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)

GPIO.output(TRIG, False)
time.sleep(2)

# ==========================
# MOBILENET SSD SETUP
# ==========================

CLASSES = [
    "background", "aeroplane", "bicycle", "bird", "boat",
    "bottle", "bus", "car", "cat", "chair", "cow",
    "diningtable", "dog", "horse", "motorbike", "person",
    "pottedplant", "sheep", "sofa", "train", "tvmonitor"
]

net = cv2.dnn.readNetFromCaffe(
    "models/MobileNetSSD_deploy.prototxt",
    "models/MobileNetSSD_deploy.caffemodel"
)

# ==========================
# DISTANCE FUNCTION
# ==========================

def get_distance():

    GPIO.output(TRIG, True)
    time.sleep(0.00001)
    GPIO.output(TRIG, False)

    pulse_start = time.time()
    pulse_end = time.time()

    timeout = time.time()

    while GPIO.input(ECHO) == 0:
        pulse_start = time.time()

        if time.time() - timeout > 0.05:
            return None

    timeout = time.time()

    while GPIO.input(ECHO) == 1:
        pulse_end = time.time()

        if time.time() - timeout > 0.05:
            return None

    pulse_duration = pulse_end - pulse_start

    distance = pulse_duration * 17150
    distance = round(distance, 2)

    if distance < 2 or distance > 400:
        return None

    return distance


# ==========================
# CAMERA
# ==========================

cap = cv2.VideoCapture(0)

try:

    while True:

        ret, frame = cap.read()

        if not ret:
            print("Camera not detected")
            break

        (h, w) = frame.shape[:2]

        # Get Distance
        distance = get_distance()

        if distance is not None:

            if distance < 50:
                status = "Very Close"
            elif distance < 150:
                status = "Near"
            else:
                status = "Far"

        else:
            status = "Unknown"

        # MobileNetSSD Detection
        blob = cv2.dnn.blobFromImage(
            cv2.resize(frame, (300, 300)),
            0.007843,
            (300, 300),
            127.5
        )

        net.setInput(blob)
        detections = net.forward()

        # Left / Center / Right guide lines
        cv2.line(frame, (w // 3, 0), (w // 3, h), (255, 0, 0), 2)
        cv2.line(frame, (2 * w // 3, 0), (2 * w // 3, h), (255, 0, 0), 2)

        # Show distance on top
        if distance is not None:
            cv2.putText(
                frame,
                f"Distance: {distance} cm | {status}",
                (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (0, 0, 255),
                2
            )

        for i in range(detections.shape[2]):

            confidence = detections[0, 0, i, 2]

            if confidence > 0.6:

                idx = int(detections[0, 0, i, 1])

                box = detections[0, 0, i, 3:7] * np.array(
                    [w, h, w, h]
                )

                (startX, startY, endX, endY) = box.astype("int")

                label = CLASSES[idx]

                center_x = (startX + endX) // 2

                if center_x < w // 3:
                    position = "Left"
                elif center_x < 2 * w // 3:
                    position = "Center"
                else:
                    position = "Right"

                text = f"{label} - {position} - {status}"

                cv2.rectangle(
                    frame,
                    (startX, startY),
                    (endX, endY),
                    (0, 255, 0),
                    2
                )

                cv2.putText(
                    frame,
                    text,
                    (startX, startY - 10),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.6,
                    (0, 255, 0),
                    2
                )

        cv2.imshow(
            "SmartVision Detection + Distance",
            frame
        )

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

finally:

    cap.release()
    cv2.destroyAllWindows()
    GPIO.cleanup()