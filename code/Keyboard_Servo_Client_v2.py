## Keyboard_Servo_Client_v2.py

import socket
import time
import keyboard

#Start netwerk connection
HOST = '192.168.4.1'
PORT = 80

#Dictionary for coding tuples
PACK_DICT={}
PACK_DICT[-1]='a'
PACK_DICT[0]='b'
PACK_DICT[1]='c'



#functions for handling keystrokes
def key_handler(key_event):
    #redirect to appropiate press or release function
    if key_event.event_type=='down':key_press_handler(key_event)
    elif key_event.event_type=='up':key_release_handler(key_event)

def key_press_handler(key_event):
    if key_event.name=='left': button_state['left']=1
    elif key_event.name=='right': button_state['right']=1

def key_release_handler(key_event):
    if key_event.name=='left': button_state['left']=0
    elif key_event.name=='right': button_state['right']=0


def sendData(data):
    #convert to string, encode and send
    dataString=PACK_DICT[data]
    dataEncoded=dataString.encode()
    s.sendall(dataEncoded)


def checkStateChange(keyDirection):
    #function for checking a change in pressed buttons
    if current_direction==keyDirection:
        return 0
    return 1


#Initialize dictionary to keep track of pressed buttons
button_state={
    'left':0,
    'right':0
}

#To keep track of the current direction
current_direction=0

#Setup connection
addr=socket.getaddrinfo(HOST, PORT)[0][4]
print(socket.getaddrinfo(HOST, PORT))
s=socket.socket()
s.connect(addr)
print(s)

#hook keyboard listerer to key_handler function
keyboard.hook(key_handler)


while True:
    #check dictionary for pressed buttons and obtain direction
    keyDirection=button_state['right']-button_state['left']
    #check if keyDirection is different from current direction
    stateChange=checkStateChange(keyDirection)

    #if keys changed send:
    if stateChange:
        sendData(keyDirection)       #send it
        current_direction=keyDirection #change direction
        time.sleep(50/1000)
