## Servo.py

import time
import board
import pulseio
from adafruit_motor import servo

# create a PWMOut object on Pin D13.
pwm = pulseio.PWMOut(board.D13, duty_cycle=2 ** 15, frequency=50)

# Create a servo object, my_servo.
my_servo = servo.Servo(pwm)

while True:
    for angle in range(0, 180, 5):  # 0 - 180 degrees, 5 degrees at a time.
        my_servo.angle = angle
        time.sleep(0.01)
    time.sleep(0.5)
    for angle in range(180, 0, -5): # 180 - 0 degrees, 5 degrees at a time.
        my_servo.angle = angle
        time.sleep(0.01)
    time.sleep(0.5)
