#!/usr/bin/python


import logging

import smbus

from pymlab.sensors import Device, SimpleBus


LOGGER = logging.getLogger(__name__)


class I2CHub(Device):
	"""Python library for I2CHUB02A MLAB module with TCA9548A i2c bus expander.

	Example:

	.. code-block:: python

		#!/usr/bin/python

		# Python library for I2CHUB02A MLAB module with TCA9548A i2c bus expander. 
		# Example code
		# Program takes two arguments

		import time
		import I2CHUB02
		import sys

		# Example of example use: 
		# sudo ./I2CHUB02_Example.py 5

		hub = I2CHUB02.i2chub(int(sys.argv[1]),eval(sys.argv[2]))

		print "Get initial I2CHUB setup:"
		print "I2CHUB channel setup:", bin(hub.status());

		#print "Setup I2CHUB to channel configuration: ", bin(hub.ch0 |hub.ch2 | hub.ch3 | hub.ch7);
		#hub.setup(hub.ch0 |hub.ch2 | hub.ch3 | hub.ch7);
		#this connect the channels O and 7 on the I2CHUB02A togeather with master bus. 

		print "Setup I2CHUB to channel configuration: ", bin(eval(sys.argv[3]));
		hub.setup(eval(sys.argv[3]));


		time.sleep(0.1);
		print "final I2C hub channel status: ", bin(hub.status());
	"""

	ch0 = 0b00000001
	ch1 = 0b00000010
	ch2 = 0b00000100
	ch3 = 0b00001000
	ch4 = 0b00010000
	ch5 = 0b00100000
	ch6 = 0b01000000
	ch7 = 0b10000000

	def __init__(self, parent = None, address=0x70, **kwargs):
		Device.__init__(self, parent, address, **kwargs)

		self.channels = {}
		for channel in range(8):
			self.channels[channel] = SimpleBus(
				self,
				None,
				channel = channel,
			)

	def __getitem__(self, key):
		return self.channels[key]

	def add_child(self, device):
		if device.channel is None:
			raise ValueError("Device doesn't have a channel.")
		self.channels[device.channel].add_child(device)
	
	def route(self, child):
		LOGGER.debug("Routing multiplexer to %r" % (child, ))
		if child.channel is None:
			LOGGER.error("Child doesn't have a channel: %r" % (child, ))
			return False
		self.setup(child.channel)
		return True

	def setup(self, i2c_channel_setup):
		self.bus.write_byte(self.address, i2c_channel_setup);
		return -1;

	def status(self):
		return self.bus.read_byte(self.address);