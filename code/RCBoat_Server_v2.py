## RCBoat_Server_v2.py

##imports
import busio
import digitalio
import time
import board
import pulseio

from micropython import const

from adafruit_esp32spi import adafruit_esp32spi
import adafruit_esp32spi.adafruit_esp32spi_socket as socket
from adafruit_motor import servo


#constant definitions
NO_SOCK_AVAIL = const(255)
PORT = 80
SSID = b'ESP32'
PASSWORD = b'JohanJohan'

##Pin definitions
#DC motor pins
ENA_PIN = board.D13
IN1_PIN = board.D12
IN2_PIN = board.D11
ENB_PIN = board.D8
IN3_PIN = board.D10
IN4_PIN = board.D9

#Servo pin
SERVO_PIN = board.D5

#Dictionary for Decoding data
UNPACK_DICT = {}
UNPACK_DICT['a'] = (0,-1)
UNPACK_DICT['b'] = (0,0)
UNPACK_DICT['c'] = (0,1)
UNPACK_DICT['d'] = (90,-1)
UNPACK_DICT['e'] = (90,0)
UNPACK_DICT['f'] = (90,1)
UNPACK_DICT['g'] = (180,-1)
UNPACK_DICT['h'] = (180,0)
UNPACK_DICT['i'] = (180,1)

#Define DC motor class
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
        if DutyC>0:
            self.forward(DutyC)
        else:
            self.backward(abs(DutyC))


##setup
#initialize servo
pwm = pulseio.PWMOut(SERVO_PIN, duty_cycle=2 ** 15, frequency=50)
my_servo = servo.Servo(pwm)
my_servo.angle=90

#initialize motors
motor1 = DC_motor(ENA_PIN,IN1_PIN,IN2_PIN)
motor2 = DC_motor(ENB_PIN,IN3_PIN,IN4_PIN)

#Obtain control over esp32
esp32_cs = digitalio.DigitalInOut(board.ESP_CS)
esp32_ready = digitalio.DigitalInOut(board.ESP_BUSY)
esp32_reset = digitalio.DigitalInOut(board.ESP_RESET)

spi = busio.SPI(board.SCK, board.MOSI, board.MISO)
esp = adafruit_esp32spi.ESP_SPIcontrol(spi, esp32_cs, esp32_ready, esp32_reset)

#create access point
esp.create_AP(SSID, PASSWORD)

#Host server
socket.set_interface(esp)
server_socket = socket.socket()
esp.start_server(PORT, server_socket.socknum)
ip = esp.pretty_ip(esp.ip_address)
print("Server available at {0}:{1}".format(ip, PORT))

#initiate client socket
client_sock = socket.socket(socknum=NO_SOCK_AVAIL)

while True:

    #wait for client connection
    while client_sock.socknum == NO_SOCK_AVAIL:
        client_sock_num = esp.socket_available(server_socket.socknum)
        client_sock = socket.socket(socknum = client_sock_num)
        if client_sock.socknum != NO_SOCK_AVAIL: print('connected')

    #once connected, recieve data
    if client_sock.connected() and client_sock.available()!= 0:
        byteData = client_sock.recv()           #recieve data
        dataString = byteData.decode()          #decode
        dataTuple = UNPACK_DICT[dataString[-1]] #last char to tuple
        print(dataTuple)
        (rudderAngle, motorvalue) = dataTuple   #unpack tuple

        #set motors
        my_servo.angle = rudderAngle
        motor1.setMotor(motorvalue)
        motor2.setMotor(motorvalue)



    # once disconnected replace client socket for
    # empty socket and wait for new client.
    elif not client_sock.connected():
        print('connection lost, looking for new connection...')
        client_sock = socket.socket(socknum = NO_SOCK_AVAIL)
