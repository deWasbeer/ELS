## Minimal_Server.py
##ESP32 docs at https://circuitpython.readthedocs.io/projects/esp32spi/en/latest/api.html

import board
import busio
from digitalio import DigitalInOut
from micropython import const
from adafruit_esp32spi import adafruit_esp32spi
import adafruit_esp32spi.adafruit_esp32spi_socket as socket


NO_SOCK_AVAIL = const(255) #255 defined by the socket library as no socket available

#setup esp32 control
esp32_cs = DigitalInOut(board.ESP_CS)
esp32_ready = DigitalInOut(board.ESP_BUSY)
esp32_reset = DigitalInOut(board.ESP_RESET)
spi = busio.SPI(board.SCK, board.MOSI, board.MISO)
esp = adafruit_esp32spi.ESP_SPIcontrol(spi, esp32_cs, esp32_ready, esp32_reset)

#Create WIFI access point
esp.create_AP(b'ESP32', b'JohanJohan')

#Setup server
port = 80
socket.set_interface(esp)
server_socket = socket.socket()
esp.start_server(port, server_socket.socknum)
ip = esp.pretty_ip(esp.ip_address)
print("Server available at {0}:{1}".format(ip, port))

#Initiate client socket
client_sock = socket.socket(socknum=NO_SOCK_AVAIL)

while True:
    #Wait for client connection
    while client_sock.socknum == NO_SOCK_AVAIL:
        client_sock_num = esp.socket_available(server_socket.socknum) #wait for request, if get request pass client socket number
        client_sock = socket.socket(socknum=client_sock_num)          #create socket object with the client socket number

    #Once connected, recieve data
    if client_sock.connected() and client_sock.available()!= 0:
        encodedData = client_sock.recv()
        data = encodedData.decode()
        print(data)

    #Once disconnected reinitiate empty client socket and wait for connection.
    elif not client_sock.connected():
        print('Connection lost, looking for new connection...')
        client_sock = socket.socket(socknum=NO_SOCK_AVAIL)
