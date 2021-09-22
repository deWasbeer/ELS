## Two_DC_Motor_Classes.py

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

#Define DC motor class
class DC_motor:
    def __init__(self,EN_pin, IN1_pin, IN2_pin):
        self.EN = pulseio.PWMOut(EN_pin)
        self.IN1 = digitalio.DigitalInOut(IN1_pin)
        self.IN1.direction = digitalio.Direction.OUTPUT
        self.IN2 = digitalio.DigitalInOut(IN2_pin)
        self.IN2.direction = digitalio.Direction.OUTPUT

    def forward(self,DutyC):
        self.EN.duty_cycle = 0
        self.IN1.value = True
        self.IN2.value = False
        self.EN.duty_cycle = int(DutyC*(2**16-1))

    def backward(self,DutyC):
        self.EN.duty_cycle = 0
        self.IN1.value = False
        self.IN2.value = True
        self.EN.duty_cycle = int(DutyC*(2**16-1))

#Create motor objects:
motor1 = DC_motor(ENA_pin,IN1_pin,IN2_pin)
motor2 = DC_motor(ENB_pin,IN3_pin,IN4_pin)

while True:
    motor1.forward(0.5)
    motor2.backward(0.3)
    time.sleep(0.5)

    motor1.backward(0.2)
    motor2.forward(0.5)
    time.sleep(0.5)
