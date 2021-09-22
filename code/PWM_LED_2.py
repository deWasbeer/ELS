## PWM_LED_2.py

#importeer modules
import pulseio
import board
import time

#initialiseer
pwm = pulseio.PWMOut(board.D13)

#Herhaal oneindig:
while True:
    for i in range(17):
        pwm.duty_cycle=2**i-1 #tot de macht i
        time.sleep(1/17)
    for i in reversed(range(17)):
        pwm.duty_cycle=2**i-1 #tot de macht i
        time.sleep(1/17)
