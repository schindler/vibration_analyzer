"""
    Mock SMBUS
"""

class SMBus(object):
    """
        SMBus
        http://blog.bitify.co.uk/2013/11/interfacing-raspberry-pi-and-mpu-6050.html
    """
    def __init__(self, V=1):
        """
        """
        self.version=V 

    def write_byte_data(self, address, reg, value):
        """
            write_byte_data
        """
        print address, reg, value

    def read_byte_data(self, address, reg):
        """
            read_byte_data
        """
        if reg == 0x75:
            return 104

        return 10
