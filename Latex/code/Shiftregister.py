## Shiftregister.py

import board
import digitalio
import time

SER_pin = board.D2
RCLK_pin = board.D4
SRCLK_pin = board.D5

SER = digitalio.DigitalInOut(SER_pin)
SER.direction = digitalio.Direction.OUTPUT
RCLK = digitalio.DigitalInOut(RCLK_pin)
RCLK.direction = digitalio.Direction.OUTPUT
SRCLK = digitalio.DigitalInOut(SRCLK_pin)
SRCLK.direction = digitalio.Direction.OUTPUT

val_register=[False for i in range(8)]



def writereg(val_register):
    RCLK.value = False

    for i in reversed(range(8)):
        SRCLK.value = False
        SER.value = val_register[i]
        SRCLK.value = True
    RCLK.value = True


writereg(val_register)

while True:
    for i in range(8):
        val_register[i] = True
        print(val_register)
        writereg(val_register)
        time.sleep(0.1)

    for i in reversed(range(8)):
        val_register[i] = False
        writereg(val_register)
        print(val_register)
        time.sleep(0.1)
