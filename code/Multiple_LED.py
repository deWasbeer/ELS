## Multiple_LED.py

# importeer modules
import board
import digitalio
import time

# initialiseer Digitale Outputs
led0 = digitalio.DigitalInOut(board.D13)
led0.direction = digitalio.Direction.OUTPUT
led1 = digitalio.DigitalInOut(board.D12)
led1.direction = digitalio.Direction.OUTPUT
led2 = digitalio.DigitalInOut(board.D11)
led2.direction = digitalio.Direction.OUTPUT
led3 = digitalio.DigitalInOut(board.D10)
led3.direction = digitalio.Direction.OUTPUT
led4 = digitalio.DigitalInOut(board.D9)
led4.direction = digitalio.Direction.OUTPUT
led5 = digitalio.DigitalInOut(board.D8)
led5.direction = digitalio.Direction.OUTPUT
led6 = digitalio.DigitalInOut(board.D7)
led6.direction = digitalio.Direction.OUTPUT
led7 = digitalio.DigitalInOut(board.D6)
led7.direction = digitalio.Direction.OUTPUT

ledlist=[led0,led1,led2,led3,led4,led5, led6, led7]


# Herhaal oneindig:
while True:
    for led in ledlist:
        led.value=True
        time.sleep(0.2)
    for led in reversed(ledlist):
        led.value=False
        time.sleep(0.2)
