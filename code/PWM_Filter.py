## PWM_Filter.py

# CircuitPython AnalogIn Demo
import time
import board
import pulseio
from analogio import AnalogIn

unfiltered_in = AnalogIn(board.A0)
filtered_in=AnalogIn(board.A1)

wave = pulseio.PWMOut(board.D13, frequency=1, duty_cycle=2**15)


def get_voltage(pin):
    return (pin.value * 3.3) / 65536


while True:
    print((get_voltage(unfiltered_in),get_voltage(filtered_in)))
    time.sleep(1/100)
