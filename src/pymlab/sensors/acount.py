#!/usr/bin/python

# Python driver for MLAB frequency counter design wrapper class

import math
import time
import sys
import struct

from pymlab.sensors import Device


class Overflow(object):
    def __repr__(self):
        return "OVERFLOW"

    def __str__(self):
        return repr(self)


OVERFLOW = Overflow()


class ACOUNTER02(Device):
    """
    Example:

    .. code-block:: python
    
        #!/usr/bin/python

        # Python library for LTS01A MLAB module with MAX31725 i2c Local Temperature Sensor

        import smbus
        import struct
        import lts01
        import sys

        I2C_bus_number = 8
        #I2CHUB_address = 0x70

        # activate I2CHUB port connected to LTS01A sensor
        #I2CHUB02.setup(I2C_bus_number, I2CHUB_address, I2CHUB02.ch0);

        LTS01A_address = 0x48

        thermometer = lts01.LTS01(int(sys.argv[1]),LTS01A_address)

        print "LTS01A status",  bin(thermometer.config())
        print "LTS01A temp", thermometer.temp()

    """

    def __init__(self, parent = None, address = 0x51, **kwargs):
        Device.__init__(self, parent, address, **kwargs)

    def read_count(self):
        b0 = self.bus.read_byte_data(self.address, 0x00)
        b1 = self.bus.read_byte_data(self.address, 0x01)
        b2 = self.bus.read_byte_data(self.address, 0x02)
        b3 = self.bus.read_byte_data(self.address, 0x03)
        count = bytes(bytearray([b3, b2, b1, b0]))
        return struct.unpack(">L", count)[0]

    def get_freq(self):
        count = self.read_count()
        return (count/9999900.0)*1e6         #convert  ~10s  of pulse counting to  frequency


if __name__ == "__main__":
    while True:
        sys.stdout.write("\r\nFrequency: " + self.get_freq() + "     ")
        sys.stdout.flush()
        time.sleep(15)
