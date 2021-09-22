## Lightsensor_TEMT6000.py

import time
import board
from analogio import AnalogIn

#initiation
analog_in = AnalogIn(board.A0)

#Convert 16-bit value to voltage
def get_voltage(pin):
    return (pin.value * 3.3) / 65535


while True:
    print((get_voltage(analog_in),))
    time.sleep(0.1)
