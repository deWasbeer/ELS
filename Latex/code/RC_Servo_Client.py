## RC_Servo_Client.py

import socket

HOST = '192.168.4.1'  # The server's hostname or IP address '192.168.4.1'
PORT = 80             # The port used by the server

addr = socket.getaddrinfo(HOST, PORT)[0][4]
print(socket.getaddrinfo(HOST, PORT))

s = socket.socket()
s.connect(addr)
print(s)

while True:
    message = input("Type na angle between 0 and 180 (-q to quit): ") #prompt
    if message == "-q": #possibility to quit the program
        break
    encodedMessage = message.encode()
    s.sendall(encodedMessage)
