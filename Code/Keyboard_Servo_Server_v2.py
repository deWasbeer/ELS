## Keyboard_Servo_Server_v2.py

##imports
import busio
from digitalio import DigitalInOut
import time
import board
import pulseio

from micropython import const

from adafruit_esp32spi import adafruit_esp32spi
import adafruit_esp32spi.adafruit_esp32spi_socket as socket
from adafruit_motor import servo


#constant definitions
NO_SOCK_AVAIL = const(255)
PORT=80
SSID=b'ESP32'
PASSWORD=b'JohanJohan'
SERVO_PIN=board.D13


#Dictionary for Decoding data
UNPACK_DICT={}
UNPACK_DICT['a']=0
UNPACK_DICT['b']=90
UNPACK_DICT['c']=180


##setup
#initiate servo
pwm = pulseio.PWMOut(SERVO_PIN, duty_cycle=2 ** 15, frequency=50)
my_servo = servo.Servo(pwm)
my_servo.angle=90


#Obtain control over esp32
esp32_cs = DigitalInOut(board.ESP_CS)
esp32_ready = DigitalInOut(board.ESP_BUSY)
esp32_reset = DigitalInOut(board.ESP_RESET)

spi = busio.SPI(board.SCK, board.MOSI, board.MISO)
esp = adafruit_esp32spi.ESP_SPIcontrol(spi, esp32_cs, esp32_ready, esp32_reset)

#create access point
esp.create_AP(SSID, PASSWORD)


#Host server
socket.set_interface(esp)
server_socket=socket.socket()
esp.start_server(PORT, server_socket.socknum)
ip = esp.pretty_ip(esp.ip_address)
print("Server available at {0}:{1}".format(ip, PORT))

#initiate client socket
client_sock = socket.socket(socknum=NO_SOCK_AVAIL)

while True:

    #wait for client connection
    while client_sock.socknum==NO_SOCK_AVAIL:
        client_sock_num=esp.socket_available(server_socket.socknum) #wait for request, if get request pass client socket number
        client_sock=socket.socket(socknum=client_sock_num)          #create socket object with the client socket number
        if client_sock.socknum!=NO_SOCK_AVAIL: print('connected')

    #once connected, recieve data
    if client_sock.connected() and client_sock.available()!=0:
        bytedata=client_sock.recv()               #recieve data
        datastring=bytedata.decode()              #convert to string
        rudderAngle=UNPACK_DICT[datastring[-1]]   #convert to string
        print(rudderAngle)
        my_servo.angle=rudderAngle                #set servo


    #once disconnected replace client socket for empty socket and wait for new client.
    elif not client_sock.connected():
        print('connection lost, looking for new connection...')
        client_sock = socket.socket(socknum=NO_SOCK_AVAIL)
