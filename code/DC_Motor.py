## DC_Motor.py

import board
import pulseio
import time
import digitalio

#Pin definitions
ENA_pin = board.D13
IN1_pin = board.D12
IN2_pin = board.D11

#Pin Initiation
ENA = pulseio.PWMOut(ENA_pin)
IN1 = digitalio.DigitalInOut(IN1_pin)
IN1.direction = digitalio.Direction.OUTPUT
IN2 = digitalio.DigitalInOut(IN2_pin)
IN2.direction = digitalio.Direction.OUTPUT

# Function definitions
def forward(DutyC):
    ENA.duty_cycle = 0
    IN1.value = True
    IN2.value = False
    ENA.duty_cycle = int(DutyC*(2**16-1))

def backward(DutyC):
    ENA.duty_cycle = 0
    IN1.value = False
    IN2.value = True
    ENA.duty_cycle = int(DutyC*(2**16-1))

while True:
    forward(0.5)
    time.sleep(0.5)
    backward(0.2)
    time.sleep(0.5)
