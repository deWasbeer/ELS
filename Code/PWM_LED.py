## PWM_LED.py

#importeer modules
import pulseio
import board

#initialiseer
pwm = pulseio.PWMOut(board.D13)
pwm.duty_cycle = 2**15-1


#Herhaal oneindig:
while True:
    pass
