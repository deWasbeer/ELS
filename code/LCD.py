## LCD.py

from lcd.lcd import LCD
from lcd.i2c_pcf8574_interface import I2CPCF8574Interface
from lcd.lcd import CursorMode
import time




# Talk to the LCD at I2C address 0x27.
lcd = LCD(I2CPCF8574Interface(board.I2C(), 0x27), num_rows=2, num_cols=16)
lcd.set_cursor_pos(0, 0)
lcd.print("Hello!\nHow are you?")
time.sleep(2)
lcd.clear()