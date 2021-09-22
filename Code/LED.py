## LED.py

#importeer modules
import board
import digitalio
import time

#initialiseer Digital Output op pin D13
led = digitalio.DigitalInOut(board.D13)
led.direction = digitalio.Direction.OUTPUT

#Herhaal oneindig:
while True:
    led.value = True #zet pin waarde hoog
    time.sleep(0.2) #wacht 0.5 seconde
    led.value = False #zet pin waarde laag
    time.sleep(0.8) #wacht 0.5 seconde
