## RCBoat_Client.py

import socket
import time
import keyboard

#Host name and port number of server
HOST = '192.168.4.1'
PORT = 80



def key_handler(key_event):
    #redirect to appropiate press or release function
    if key_event.event_type == 'down':key_press_handler(key_event)
    elif key_event.event_type == 'up':key_release_handler(key_event)


def key_press_handler(key_event):
    if key_event.name == 'left': button_state['left'] = 1
    elif key_event.name == 'right': button_state['right'] = 1
    elif key_event.name == 'up': button_state['forward'] = 1
    elif key_event.name == 'down': button_state['backward'] = 1

def key_release_handler(key_event):
    if key_event.name == 'left': button_state['left'] = 0
    elif key_event.name == 'right': button_state['right'] = 0
    elif key_event.name == 'up': button_state['forward'] = 0
    elif key_event.name == 'down': button_state['backward'] = 0

def sendData(data):
    #convert to string, encode and send
    dataString = str(data)
    dataEncoded = dataString.encode()
    s.sendall(dataEncoded)


def checkStateChange(keyDirection):
    if current_direction == keyDirection:
        return 0
    return 1


#Initialize dictionary to keep track of pressed buttons
button_state = {
    'left':0,
    'right':0,
    'forward':0,
    'backward':0
}

#To keep track of the current direction
current_direction = (0,0)

#convert to host and port to address
addr = socket.getaddrinfo(HOST, PORT)[0][4]
print(socket.getaddrinfo(HOST, PORT))

#connect to address
s = socket.socket()
s.connect(addr)
print(s)

#hook keyboard listerer to key_handler function
keyboard.hook(key_handler)



while True:
    #check dictionary
    leftRightDirection = button_state['right']-button_state['left']
    upDownDirection = button_state['forward']-button_state['backward']
    keyDirection = (leftRightDirection,upDownDirection)
    #check if keyDirection is changed
    stateChange = checkStateChange(keyDirection)

    #if it is changed:
    if stateChange:
        current_direction = keyDirection #change direction
        sendData(current_direction)       #send it
        time.sleep(50/1000)
