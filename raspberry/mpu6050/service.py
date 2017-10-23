"""
    Service to read data from Sensor and save
"""
import time

import data
import mpu6050

if __name__ == "__main__":
    STORE = data.Store()
    SENSOR = mpu6050.Sensor()
    DELAY = 1.0/1000.0

    start = time.time()     
    rows = []

    for i in xrange(0,100):
        rows.append(SENSOR.data())
        time.sleep(DELAY)

    print time.time() - start
     
    start = time.time()
    STORE.add_all(rows)

    
    print len(rows), time.time() - start
