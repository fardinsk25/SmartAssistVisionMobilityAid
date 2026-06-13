import RPi.GPIO as GPIO
import time

TRIG = 23
ECHO = 24

GPIO.setmode(GPIO.BCM)
GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)

GPIO.output(TRIG, False)

print("Waiting for sensor...")
time.sleep(2)

try:
    while True:

        # Send trigger pulse
        GPIO.output(TRIG, True)
        time.sleep(0.00001)
        GPIO.output(TRIG, False)

        pulse_start = time.time()
        pulse_end = time.time()

        # Wait for echo to go HIGH
        timeout = time.time()
        while GPIO.input(ECHO) == 0:
            pulse_start = time.time()

            if time.time() - timeout > 0.05:
                break

        # Wait for echo to go LOW
        timeout = time.time()
        while GPIO.input(ECHO) == 1:
            pulse_end = time.time()

            if time.time() - timeout > 0.05:
                break

        pulse_duration = pulse_end - pulse_start

        distance = pulse_duration * 17150
        distance = round(distance, 2)

        # Ignore invalid readings
        if distance < 2 or distance > 400:
            continue

        # Distance classification
        if distance < 50:
            status = "Very Close"
        elif distance < 150:
            status = "Near"
        else:
            status = "Far"

        print(f"Distance: {distance} cm | Status: {status}")

        time.sleep(0.5)

except KeyboardInterrupt:
    print("\nProgram stopped")
    GPIO.cleanup()
