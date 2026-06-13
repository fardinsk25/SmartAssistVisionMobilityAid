import cv2
import numpy as np
import RPi.GPIO as GPIO
import time
import os

# =====================================
# HC-SR04 SETUP
# =====================================

TRIG = 23
ECHO = 24

GPIO.setmode(GPIO.BCM)
GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)

GPIO.output(TRIG, False)
time.sleep(2)

# =====================================
# MobileNetSSD Classes
# =====================================

CLASSES = [
    "background", "aeroplane", "bicycle", "bird", "boat",
    "bottle", "bus", "car", "cat", "chair", "cow",
    "diningtable", "dog", "horse", "motorbike", "person",
    "pottedplant", "sheep", "sofa", "train", "tvmonitor"
]

DISPLAY_NAMES = {
    "diningtable": "table",
    "tvmonitor": "monitor",
    "motorbike": "bike",
    "pottedplant": "plant"
}

# =====================================
# LOAD MODEL
# =====================================

net = cv2.dnn.readNetFromCaffe(
    "models/MobileNetSSD_deploy.prototxt",
    "models/MobileNetSSD_deploy.caffemodel"
)

# =====================================
# DISTANCE FUNCTION
# =====================================

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

# =====================================
# CAMERA
# =====================================

cap = cv2.VideoCapture(0)

cap.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)

# =====================================
# SPEECH SETTINGS
# =====================================

last_message = ""
last_spoken_time = 0

candidate_message = ""
candidate_start_time = 0

SPEAK_DELAY = 0.7
COOLDOWN = 2

# =====================================
# DISTANCE CACHE
# =====================================

distance = None
status = "unknown"
last_distance_time = 0

# =====================================
# DETECTION CACHE
# =====================================

best_message = ""
best_box = None

frame_count = 0

try:

    while True:

        ret, frame = cap.read()

        if not ret:
            print("Camera not detected")
            break

        (h, w) = frame.shape[:2]

        current_time = time.time()

        # =============================
        # DISTANCE UPDATE
        # =============================

        if current_time - last_distance_time > 0.5:

            distance = get_distance()

            if distance is None:
                status = "unknown"

            elif distance < 50:
                status = "very close"

            elif distance < 150:
                status = "near"

            else:
                status = "far"

            last_distance_time = current_time

        # =============================
        # OBJECT DETECTION
        # =============================

        frame_count += 1

        if frame_count % 2 == 0:

            blob = cv2.dnn.blobFromImage(
                cv2.resize(frame, (300, 300)),
                0.007843,
                (300, 300),
                127.5
            )

            net.setInput(blob)
            detections = net.forward()

            largest_area = 0
            current_message = ""
            current_box = None

            for i in range(detections.shape[2]):

                confidence = detections[0, 0, i, 2]

                if confidence < 0.60:
                    continue

                idx = int(detections[0, 0, i, 1])

                label = CLASSES[idx]
                label = DISPLAY_NAMES.get(label, label)

                box = detections[0, 0, i, 3:7] * np.array(
                    [w, h, w, h]
                )

                (startX, startY, endX, endY) = box.astype("int")

                area = (endX - startX) * (endY - startY)

                if area > largest_area:

                    largest_area = area

                    center_x = (startX + endX) // 2

                    if center_x < w // 3:
                        position = "left"
                    elif center_x < 2 * w // 3:
                        position = "center"
                    else:
                        position = "right"

                    if status == "far":
                        current_message = f"{label} ahead"

                    elif status == "near":
                        current_message = f"{label} on {position}"

                    else:
                        current_message = f"caution {label} very close"

                    current_box = (
                        startX,
                        startY,
                        endX,
                        endY
                    )

            if current_message:
                best_message = current_message
                best_box = current_box

        # =============================
        # SPEECH LOGIC
        # =============================

        current_time = time.time()

        if best_message:

            if best_message != candidate_message:

                candidate_message = best_message
                candidate_start_time = current_time

            elif (
                current_time - candidate_start_time >= SPEAK_DELAY
                and current_time - last_spoken_time >= COOLDOWN
                and best_message != last_message
            ):

                print("Speaking:", best_message)

                os.system(
                    f'espeak -s 120 "{best_message}" >/dev/null 2>&1 &'
                )

                last_message = best_message
                last_spoken_time = current_time

        # =============================
        # DISPLAY
        # =============================

        cv2.line(frame, (w // 3, 0), (w // 3, h), (255, 0, 0), 1)
        cv2.line(frame, (2 * w // 3, 0), (2 * w // 3, h), (255, 0, 0), 1)

        if distance is not None:

            cv2.putText(
                frame,
                f"{distance:.1f} cm | {status}",
                (10, 20),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.5,
                (0, 0, 255),
                2
            )

        if best_box is not None:

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
                best_message,
                (startX, max(20, startY - 10)),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.45,
                (0, 255, 0),
                2
            )

        cv2.imshow("Smart Vision Assistant", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

finally:

    cap.release()
    cv2.destroyAllWindows()
    GPIO.cleanup()