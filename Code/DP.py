#Distance_twice.py
import time
import board
import adafruit_hcsr04
from math import atan, cos, pi
import sys
import pulseio
import digitalio


MAX_X_ERROR=0.03
MAX_Y_ERROR=0.03
MAX_ROT_ERROR=3/180*pi #radians
MAX_ERRORS=(MAX_X_ERROR,MAX_Y_ERROR,MAX_ROT_ERROR)


BOAT_LENGTH = 0.5
BOAT_WIDTH = 0.2
SONAR_FRONT_POS = (-0.0,0.03)
SONAR_BACK_POS = (-0.0,-0.03)
SONAR_REAR_POS = (0,-0.05)
DCMOTOR_RIGHT_POS = (0.15, -0.25)
DCMOTOR_LEFT_POS = (-0.15, -0.25)
BOWTHR_POS = (0,0.2)

#initiate 2 ultrasonic sensors
sonarSideFront = adafruit_hcsr04.HCSR04(trigger_pin=board.D5, echo_pin=board.D6)
sonarSideBack = adafruit_hcsr04.HCSR04(trigger_pin=board.D7, echo_pin=board.D8)
sonarRear = adafruit_hcsr04.HCSR04(trigger_pin=board.D4, echo_pin=board.D3)



def getPos():
    sensorValues = (sonarSideFront.distance/100, sonarSideBack.distance/100, 0.02)#sonarRear.distance)
    #print(sensorValues)
    x = (sensorValues[0]+SONAR_FRONT_POS[0]+sensorValues[1]+SONAR_BACK_POS[0])/2
    rot = -atan((sensorValues[0]-sensorValues[1])/(SONAR_FRONT_POS[1]-SONAR_BACK_POS[1])) #radians
    y = sensorValues[2]*cos(rot)-SONAR_REAR_POS[1]
    #print(x,y,rot/pi*180)
    return (x, y, rot)

def ConvertToMotorDuty(Fx,Fy,M):
    # x direction part
    bow_x = Fx
    right_x = BOWTHR_POS[1]*bow_x/(2*DCMOTOR_RIGHT_POS[0])
    left_x = -right_x

    # y direction part
    right_y = Fy
    left_y = Fy

    # rotational part
    right_rot = M
    left_rot = -M

    dutyTuple = (right_x + right_y + right_rot, left_x + left_y + left_rot, bow_x)
    absMax = max([abs(x) for x in dutyTuple])
    #print(dutyTuple, absMax)
    if absMax > 1: dutyTuple = tuple(duty / absMax for duty in dutyTuple)

    return dutyTuple

class PID:
    def __init__(self, kp, kd, ki, tf, limit = 0):
        self.kp = kp
        self.kd = kd
        self.ki = ki
        self.tf = tf
        if limit == 0:self.limit = sys.maxsize
        else: self.limit = limit
        self.prevtime = time.time_ns()*1e-9
        self.Iout = 0
        self.prev_error = 0 #maybe change

    def calculate(self, setpoint, currentPos):
        newtime = time.time_ns() * 1e-9
        dt = newtime - self.prevtime                    #time since last cycle
        error = setpoint - currentPos                   #difference between setpoint and current position
        Pout = self.kp * error                          #proportional part

        derivative = (error - self.prev_error) / dt;          #derivative
        Dout = self.kd * derivative / (self.tf * derivative + 1); #PID derivative part


        self.Iout += self.ki * error * dt;                            #integral part
        if (self.Iout > self.limit): self.Iout = self.limit;         #anti-windup of integrator
        elif (self.Iout < -self.limit): self.Iout = -self.limit;    #"      "

        output = Pout + self.Iout + Dout;                             #add all PID parts together

        #limit output to maximum output motor
        if(output > self.limit): output = self.limit;
        elif(output < -self.limit): output = -self.limit;

        #store values
        self.prev_error = error;
        self.prevtime = newtime;

        return output;

class PID2:
    #https://drive.google.com/uc?export=download&id=1fI8DBGXx_P8KYgzJsU-Y10nbDZJT4a5t
    def __init__(self, kp, kd, ki, limit=0):
        self.k1 = kp + ki + kd
        self.k2 = -kp - 2 * kd
        self.k3 = kd
        #self.tf=tf
        if limit==0:self.limit=sys.maxsize
        else: self.limit=limit
        #self.prevtime=time.time_ns()*1e-9
        self.u=0
        self.e2=0
        self.e1=0
        self.e=0

    def calculate(self, setpoint, currentPos):
        self.e2 = self.e1
        self.e1 = self.e
        self.e = setpoint-currentPos
        delta_u = self.k1 * self.e + self.k2 * self.e1 + self.k3 * self.e2
        self.u = self.u + delta_u
        if self.u > self.limit: self.u = self.limit
        if self.u < -self.limit: self.u = -self.limit
        return self.u

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
        self.EN.duty_cycle = int(DutyC * (2 ** 16 - 1))

    def backward(self, DutyC):
        self.EN.duty_cycle = 0
        self.IN1.value = False
        self.IN2.value = True
        self.EN.duty_cycle = int(DutyC * (2 ** 16 - 1))

    def setMotor(self, DutyC):
        if DutyC > 0:
            self.forward(DutyC)
        else:
            self.backward(abs(DutyC))

#DC_right = DC_motor(board.D13, board.D12, board.D11)
#DC_left = DC_motor(board.D10, board.D9, board.D4)
#DC_bow = DC_motor(board.D3, board.D2, board.D1)


#xPID=PID(1/3,0,0,0)
xPID = PID2(0.1, 0, 0)
yPID = PID2(0.1, 0, 0)
rotPID = PID2(0.1, 0, 0)

(xRef, yRef, rotRef) = (0, 0, 0)

while (xRef, yRef, rotRef) == (0, 0, 0):
    try: (xRef, yRef, rotRef) = tuple(ref/max_e for ref, max_e in zip(getPos(),MAX_ERRORS)) #normalized
    except: (xRef, yRef, rotRef) = (0, 0, 0)

print(xRef, yRef, rotRef)

while True:
    try: (xPos, yPos, rot) = tuple(pos/max_e for pos, max_e in zip(getPos(),MAX_ERRORS))
    except: continue
    (Fx,Fy,M) = (xPID.calculate(xRef, xPos), yPID.calculate(yRef, yPos), rotPID.calculate(rotRef, rot))
    (dutyRight, dutyLeft, dutyBow) = ConvertToMotorDuty(Fx,Fy,M)
    print(dutyRight, dutyLeft, dutyBow)
    #DC_right.setMotor(dutyRight)
    #DC_left.setMotor(dutyLeft)
    #DC_bow.setMotor(dutyBow)
    time.sleep(0.1)
