#Distance_twice.py
import time
import board
import adafruit_hcsr04

#initiate 2 ultrasonic sensors
sonar1 = adafruit_hcsr04.HCSR04(trigger_pin=board.D5, echo_pin=board.D6)
sonar2 = adafruit_hcsr04.HCSR04(trigger_pin=board.D7, echo_pin=board.D8)

while True:
  try:
      print((sonar1.distance,sonar2.distance))
  except RuntimeError:
      print("Retrying!")
  time.sleep(0.1)
