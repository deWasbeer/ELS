## WIFI_AccessPoint.py

#imports
import board
import busio
from digitalio import DigitalInOut
from adafruit_esp32spi import adafruit_esp32spi


#setup ESP32 control
esp32_cs = DigitalInOut(board.ESP_CS)
esp32_ready = DigitalInOut(board.ESP_BUSY)
esp32_reset = DigitalInOut(board.ESP_RESET)
spi = busio.SPI(board.SCK, board.MOSI, board.MISO)
esp = adafruit_esp32spi.ESP_SPIcontrol(spi, esp32_cs, esp32_ready, esp32_reset)

#Create WIFI access point
esp.create_AP('Accespoint_Name', 'Password')

#Do nothing
while True: pass
