# Two_DC_Motors_Servo_Joystick.py

import board
import pulseio
import time
import digitalio
from analogio import AnalogIn
from adafruit_motor import servo
import simpleio

# Pin definitions
# DC motor pins
ENA_pin = board.D13
IN1_pin = board.D12
IN2_pin = board.D11
ENB_pin = board.D8
IN3_pin = board.D10
IN4_pin = board.D9

# Servo pin
servo_pin = board.D5

# Joystick pins
joy_LeftRight_pin = board.A1
joy_UpDown_pin = board.A0
joy_button_pin = board.D6

# Horn pin
horn_pin = board.D7


# Define DC motor class
class DC_motor:
    def __init__(self, EN_pin, IN1_pin, IN2_pin):
        self.EN = pulseio.PWMOut(EN_pin)
        self.IN1 = digitalio.DigitalInOut(IN1_pin)
        self.IN1.direction = digitalio.Direction.OUTPUT
        self.IN2 = digitalio.DigitalInOut(IN2_pin)
        self.IN2.direction = digitalio.Direction.OUTPUT

    def forward(self, DutyC):
        self.EN.duty_cycle = 0
        self.IN1.value = True
        self.IN2.value = False
        self.EN.duty_cycle = int(DutyC*(2**16-1))

    def backward(self, DutyC):
        self.EN.duty_cycle = 0
        self.IN1.value = False
        self.IN2.value = True
        self.EN.duty_cycle = int(DutyC*(2**16-1))

    def setMotor(self, DutyC):
        if DutyC > 0:
            self.forward(DutyC)
        else:
            self.backward(abs(DutyC))


def toDutyCycle(bitValue):
    # map 0-3,3V van joystick naar -3,3 tot 3,3V voor motors
    return (bitValue*2-(2**16-1))/(2**16-1)

def toAngle(bitValue):
    # bitvalue naar servo hoek
    return bitValue/(2**16-1)*180

def setHorn(buttonpressed):
    # als wel ingedrukt duty_cycle 50%
    if buttonpressed:
        simpleio.tone(horn_pin, 400, 0.1)
        time.sleep(0.1)
        simpleio.tone(horn_pin, 400, 0.1)
        time.sleep(0.1)

# Initiatization
# Create motor objects:
motor1 = DC_motor(ENA_pin, IN1_pin, IN2_pin)
motor2 = DC_motor(ENB_pin, IN3_pin, IN4_pin)

# Create Servo object
pwm = pulseio.PWMOut(servo_pin, duty_cycle=2 ** 15, frequency=50)
my_servo = servo.Servo(pwm)

# Initialize joystick pins
joy_button = digitalio.DigitalInOut(joy_button_pin)
joy_button.direction = digitalio.Direction.INPUT
joy_button.pull = digitalio.Pull.UP

joy_LeftRight = AnalogIn(joy_LeftRight_pin)
joy_UpDown = AnalogIn(joy_UpDown_pin)


while True:
    # Read out and convert joystick values
    LeftRightAngle = toAngle(joy_LeftRight.value)
    UpDownDutyC = toDutyCycle(joy_UpDown.value)
    ButtonState = not joy_button.value

    # set DC motors, servo and claxxon
    my_servo.angle = LeftRightAngle
    motor1.setMotor(UpDownDutyC)
    motor2.setMotor(UpDownDutyC)
    setHorn(ButtonState)