## Minimal_Client.py

import socket

#Host name and port number of server
HOST = '192.168.4.1'
PORT = 80

#convert to host and port to address
addr=socket.getaddrinfo(HOST, PORT)[0][4]
print(socket.getaddrinfo(HOST, PORT))

#connect to address
s=socket.socket()
s.connect(addr)
print(s)

while True:
    message=input("Type a message (-q to quit): ")
    if message=="-q": #possibility to quit the program
        quit()
    encodedMessage=message.encode()
    s.sendall(encodedMessage)
