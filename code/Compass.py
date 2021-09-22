# sort of works

import time
import board
import busio
from mpu9250_CP import MPU9250
from math import atan2, pi

#from adafruit_bus_device.i2c_device import I2CDevice
if __name__=='__main__':
    with busio.I2C(board.SCL, board.SDA) as i2c:
        #mpu6500_CP.MPU6500(i2c)
        sensor = MPU9250(i2c)
        sensor.ak8963._offset=(-2800, -2400, 0)       #offset and scaling very important
        sensor.ak8963._scale=(1/220, 1/200, 1.03659)
        #sensor.ak8963.calibrate()
        print(sensor.ak8963._offset,sensor.ak8963._scale)
        while True:
            #print(sensor.acceleration)
            #print(sensor.gyro)
            value=[0,0,0]
            for i in range(100):
                value=[sum(x) for x in zip(value, list(sensor.magnetic))]
            value=tuple([x/100 for x in value])
            heading=atan2(-value[1],value[0])*180/pi
            #print((value[1],))
            print((heading,))
            #print("")
            time.sleep(0.1)
