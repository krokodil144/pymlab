#!/usr/bin/python

#import smbus
import time
import sys

from pymlab.sensors import Device


#TODO: Implement output data checksum checking 

class SHT25(Device):
    'Python library for SHT25v01A MLAB module with Sensirion SHT25 i2c humidity and temperature sensor.'

    def __init__(self, parent = None, address = 0x40, **kwargs):
        Device.__init__(self, parent, address, **kwargs)

        self.SHT25_HEATER_ON = 0x04
        self.SHT25_HEATER_OFF = 0x00
        self.SHT25_OTP_reload_off = 0x02
        self.SHT25_RH12_T14 = 0x00 
        self.SHT25_RH8_T12 = 0x01
        self.SHT25_RH10_T13 = 0x80
        self.SHT25_RH11_T11 = 0x81
        #self.address = 0x40    # SHT25 has only one device address (factory set)

        self.TRIG_T_HOLD = 0b11100011
        self.TRIG_RH_HOLD = 0b11100101
        self.TRIG_T_noHOLD = 0b11110011
        self.TRIG_RH_noHOLD = 0b11110101
        self.WRITE_USR_REG = 0b11100110
        self.READ_USR_REG = 0b11100111
        self.SOFT_RESET = 0b11111110

    def soft_reset(self):
        self.bus.write_byte(self.address, self.SOFT_RESET);
        return

    def setup(self, setup_reg ):  # writes to status register and returns its value
        reg=self.bus.read_byte_data(self.address, self.READ_USR_REG);    # Read status actual status register
        reg = (reg & 0x3A) | setup_reg;    # modify actual register status leave reserved bits without modification
        self.bus.write_byte_data(self.address, self.WRITE_USR_REG, reg); # write new status register
        return self.bus.read_byte_data(self.address, self.READ_USR_REG);    # Return status actual status register for check purposes

    def get_temp(self):
        self.bus.write_byte(self.address, self.TRIG_T_noHOLD); # start temperature measurement
        time.sleep(0.1)

        data = self.bus.read_i2c_block(self.address, 2) # Sensirion digital sensors are pure I2C devices, therefore clear I2C trasfers must be used instead of SMBus trasfers.

        value = data[0]<<8 | data[1]
        value &= ~0b11    # trow out status bits
        return(-46.85 + 175.72*(value/65536.0))

    def get_hum(self, raw = False):
        """
        The physical value RH given above corresponds to the
        relative humidity above liquid water according to World
        Meteorological Organization (WMO)
        """
        self.bus.write_byte(self.address, self.TRIG_RH_noHOLD); # start humidity measurement
        time.sleep(0.1)

        data = self.bus.read_i2c_block(self.address, 2)

        value = data[0]<<8 | data[1]
        value &= ~0b11    # trow out status bits
        humidity = (-6.0 + 125.0*(value/65536.0))

        if raw:                 # raw sensor output, useful for getting an idea of sensor failure status
            return humidity

        else: 

            if humidity > 100.0:        # limit values to relevant physical variable (values out of that limit is sensor error state and are dependent on specific sensor piece)
                return 100.0
            elif humidity < 0.0:
                return 0.0
            else: 
                return humidity

class SHT31(Device):
    'Python library for SHT31v01A MLAB module with Sensirion SHT31 i2c humidity and temperature sensor.'

    def __init__(self, parent = None, address = 0x44, **kwargs):
        Device.__init__(self, parent, address, **kwargs)

        self.SOFT_RESET = [0x30, 0xA2]
        self.STATUS_REG = [0xF3, 0x2D]
        self.MEASURE_H_CLKSD = [0x24, 0x00]

    def soft_reset(self):
        self.bus.write_i2c_block(self.address, self.SOFT_RESET);
        return

    def get_status(self):
        self.bus.write_i2c_block(self.address, self.STATUS_REG)
        status = self.bus.read_i2c_block(self.address, 3)
        bits_values = dict([('Invalid_checksum',status[0] & 0x01 == 0x01),
                    ('Invalid_command',status[0] & 0x02 == 0x02),
                    ('System_reset',status[0] & 0x10 == 0x10),
                    ('T_alert',status[1] & 0x04 == 0x04),
                    ('RH_alert',status[1] & 0x08 == 0x08),
                    ('Heater',status[1] & 0x20 == 0x02),
                    ('Alert_pending',status[1] & 0x80 == 0x80),
                    ('Checksum',status[2])])
        return bits_values


    def get_TempHum(self):        
        self.bus.write_i2c_block(self.address, self.MEASURE_H_CLKSD); # start temperature and humidity measurement
        time.sleep(0.05)

        data = self.bus.read_i2c_block(self.address, 6)

        temp_data = data[0]<<8 | data[1]
        hum_data = data[3]<<8 | data[4]

        humidity = 100.0*(hum_data/65535.0)
        temperature = -45.0 + 175.0*(temp_data/65535.0) 

        return temperature, humidity


    @staticmethod
    def _calculate_checksum(value):
        """4.12 Checksum Calculation from an unsigned short input"""
        # CRC
        polynomial = 0x131  # //P(x)=x^8+x^5+x^4+1 = 100110001
        crc = 0xFF

        # calculates 8-Bit checksum with given polynomial
        for byteCtr in [ord(x) for x in struct.pack(">H", value)]:
            crc ^= byteCtr
            for bit in range(8, 0, -1):
                if crc & 0x80:
                    crc = (crc << 1) ^ polynomial
                else:
                    crc = (crc << 1)
        return crc

def main():
    print __doc__


if __name__ == "__main__":
    main()
