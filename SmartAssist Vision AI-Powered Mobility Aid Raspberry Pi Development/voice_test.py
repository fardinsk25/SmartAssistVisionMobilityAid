import os
import time

messages = [
    "Person on the left near",
    "Chair in center very close",
    "Bottle on the right far"
]

for msg in messages:
    print(msg)
    os.system(f'espeak "{msg}"')
    time.sleep(2)
