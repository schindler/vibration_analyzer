"""
    Service to read data from Sensor and save
"""
import data
import mpu6050

if __name__ == "__main__":
    STORE = data.Store()
    SENSOR = mpu6050.Sensor()
    DELAY = 1.0/1000.0
    while True: 

        for i in xrange(0, 1000):
            STORE.add(SENSOR.data())
            #time.sleep(DELAY)

        STORE.commit()
