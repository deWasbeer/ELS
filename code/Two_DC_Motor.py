## Two_DC_Motor.py

import board
import pulseio
import time
import digitalio

#Define pins
ENA_pin = board.D13
IN1_pin = board.D12
IN2_pin = board.D11
ENB_pin = board.D8
IN3_pin = board.D10
IN4_pin = board.D9

#initialize DC motor pins
ENA = pulseio.PWMOut(ENA_pin)
IN1 = digitalio.DigitalInOut(IN1_pin)
IN1.direction = digitalio.Direction.OUTPUT
IN2 = digitalio.DigitalInOut(IN2_pin)
IN2.direction = digitalio.Direction.OUTPUT

ENB = pulseio.PWMOut(ENB_pin)
IN3 = digitalio.DigitalInOut(IN3_pin)
IN3.direction = digitalio.Direction.OUTPUT
IN4 = digitalio.DigitalInOut(IN4_pin)
IN4.direction = digitalio.Direction.OUTPUT


def DC1_forward(DutyC):
    ENA.duty_cycle = 0
    IN1.value = True
    IN2.value = False
    ENA.duty_cycle = int(DutyC*(2**16-1))

def DC1_backward(DutyC):
    ENA.duty_cycle = 0
    IN1.value = False
    IN2.value = True
    ENA.duty_cycle = int(DutyC*(2**16-1))

def DC2_forward(DutyC):
    ENB.duty_cycle = 0
    IN3.value = True
    IN4.value = False
    ENB.duty_cycle = int(DutyC*(2**16-1))

def DC2_backward(DutyC):
    ENB.duty_cycle = 0
    IN3.value = False
    IN4.value = True
    ENB.duty_cycle = int(DutyC*(2**16-1))

while True:
    DC1_forward(0.5)
    DC2_backward(0.3)
    time.sleep(0.5)

    DC1_backward(0.2)
    DC2_forward(0.5)
    time.sleep(0.5)
