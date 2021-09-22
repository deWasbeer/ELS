## Joystick.py

import time
import board
from digitalio import DigitalInOut, Direction, Pull
from analogio import AnalogIn

#initialize joystick analog pins
LeftRight_Reading = AnalogIn(board.A1)
UpDown_Reading = AnalogIn(board.A0)

#initialize joystick pressdown switch
switch = DigitalInOut(board.D7)
switch.direction = Direction.INPUT
switch.pull = Pull.UP

#define function to readout voltage
def get_voltage(pin):
    return (pin.value * 3.3) / 65535


while True:
    if switch.value: #if button is not pressed
        print((get_voltage(LeftRight_Reading),get_voltage(UpDown_Reading)))
    else:           #if button is pressed
        print("button pressed")
    time.sleep(0.1)
