"""
  MPU6050 Module
"""
try:
    import smbus
except ImportError:
    #Probably running test cases
    import mocksmbus as smbus

class Sensor(object):
    """
        Basic configuration
        https://www.invensense.com/wp-content/uploads/2015/02/MPU-6000-Register-Map1.pdf

        GPIO Raspberry Pi 3 V2
        Pin 1 - 3.3V connect to VCC
        Pin 3 - SDA connect to SDA
        Pin 5 - SCL connect to SCL
        Pin 6 - Ground connect to GND
    """

    def __init__(self, adr=0x68, V=1):
        self.power_mgmt_1 = 0x6b
        self.power_mgmt_2 = 0x6c
        self.acceleration_config_scale = 0x1C
        self.address = adr
        self.bus = smbus.SMBus(V)
        assert self.read(0x75) == 104, "MPU6050 Not Found"

        self.bus.write_byte_data(adr, self.power_mgmt_1, 0)
        self.bus.write_byte_data(adr, self.acceleration_config_scale, 0)

    def read(self, reg):
        """
        Reads a single byte from I2C Bus
        """
        return self.bus.read_byte_data(self.address, reg)

    def read_word(self, reg):
        """
        Reads two bytes as an integer
        """
        return (self.read(reg) << 8) + self.read(reg+1)

    def read_short(self, reg):
        """
          Convertes read_word to signed int
        """
        value = self.read_word(reg)
        return value if value < 0x8000 else -((65535-value)+1)

    def temperature(self):
        """
          Reads temperature em Celcius
        """
        return self.read_short(65) / 340.0 + 36.53

    def acceleration(self):
        """
          Reads acceleration g
        """
        return [(self.read_short(i) / 16384.0) for i in xrange(59, 65, 2)]

    def data(self):
        """
          Reads acceleration and temperature
        """
        return (self.read_short(59), self.read_short(61), self.read_short(63), self.temperature())
