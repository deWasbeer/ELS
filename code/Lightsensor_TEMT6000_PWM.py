## Lightsensor_TEMT6000_PWM.py

import time
import pulseio
import board
from analogio import AnalogIn

#initiation
pwm = pulseio.PWMOut(board.D13)
analog_in = AnalogIn(board.A0)

#Convert 16-bit value to voltage
def get_voltage(pin):
    return (pin.value * 3.3) / 65535


while True:
    pwm.duty_cycle=65535-(analog_in.value) #donkerder is feller
    print((get_voltage(analog_in),))
    time.sleep(0.1)
