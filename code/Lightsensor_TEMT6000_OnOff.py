## Ligthsensor_TEMT600_OnOff.py

import time
import board
import digitalio
from analogio import AnalogIn

#initiate pins
led = digitalio.DigitalInOut(board.D13)
led.direction = digitalio.Direction.OUTPUT
analog_in = AnalogIn(board.A0)

#convert 16-bit value to voltage
def get_voltage(pin):
    return (pin.value * 3.3) / 65535


while True:
    if analog_in.value < (63536/2):
        led.value = True
    else:
        led.value = False
    print((get_voltage(analog_in),))
    time.sleep(0.1)
