"""
 Test Module
"""
import datetime
import time

import mpu6050

if __name__ == "__main__":
    MPU = mpu6050.Sensor()
    for i in xrange(0, 60):
        print str(datetime.datetime.now())+":"+str(MPU.temperature())
        time.sleep(60)
