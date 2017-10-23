"""
    Service to read data from Sensor and save
"""
import time

import data
import mpu6050

if __name__ == "__main__":
    STORE = data.Store()
    SENSOR = mpu6050.Sensor()
    DELAY = 5.0/1000.0

    for tt in xrange (0, 3):
        start = time.time()     

        for i in xrange(0,1000):
            STORE.add(SENSOR.data())
            time.sleep(DELAY)

        STORE.commit()

        print time.time() - start
