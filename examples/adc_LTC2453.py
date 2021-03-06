#!/usr/bin/python

# Python example of use pymlab with LIONCELL01 MLAB module

import time
import sys
from pymlab import config

while True:
    #### Sensor Configuration ###########################################
    cfg = config.Config(
        i2c = {
            "port": 0, # I2C bus number
        },

	    bus = [
                {
                 "name": "adc",
                 "type": "LTC2453", 
                 #"channel": 7, 
                },
            ],
    )


    cfg.initialize()
    adc = cfg.get_device("adc")

    Ra = 4700.0     # Circuit Constants opitmized for PT100 sensor.  
    Rb = 1500.0
    N = 16

    try:
        while True:
            # Voltage readout
            adc_value = adc.readADC()
            Rpt100 = Ra * adc_value /(2**(N-1) - adc_value)
            Vref = (Ra + Rpt100)/(Ra + Rb + Rpt100)
            Vpt100 = Vref * adc_value / 2**(N-1)
            sys.stdout.write("ADC: %d Rpt100: %.2f  Vpt100: %.6f \n" % (adc_value, Rpt100, Vpt100))
            sys.stdout.flush()

            time.sleep(1)

    except IOError:
        print "IOError"
        continue

    except KeyboardInterrupt:
    	sys.exit(0)
