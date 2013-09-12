#!/usr/bin/python

import smbus

# Based on Adafruit_I2C
# https://github.com/adafruit/Adafruit-Raspberry-Pi-Python-Code/

class I2C :

	def __init__(self, address):
		self.address = address

		try:
		 with open('/proc/cpuinfo','r') as f:
		  for line in f:
		   if line.startswith('Revision'):
		    b = 0 if line.rstrip()[-1] in ['1','2'] else 1
		except:
		 b = 0
		self.bus = smbus.SMBus(b)

	def errMsg(self):
		print "Error accessing 0x%02X" % self.address
		return -1

	def write8(self, reg, value):
		try:
		 self.bus.write_byte_data(self.address, reg, value)
		except IOError, err:
		 return self.errMsg()

	def write16(self, reg, value):
		try:
		 self.bus.write_word_data(self.address, reg, value)
		except IOError, err:
		 return self.errMsg()

	def read8(self, reg, signed=False):
		try:
		 result = self.bus.read_byte_data(self.address, reg)
		 if signed and result > 0x7F: result -= 0xFF
		 return result
		except IOError, err:
		 return self.errMsg()

	def read16(self, reg, signed=False):
		try:
		 hi = self.bus.read_byte_data(self.address, reg)
		 lo = self.bus.read_byte_data(self.address, reg+1)
		 if signed and hi > 0x7F: hi -= 0xFF
		 return (hi<<8)+lo
		except IOError, err:
		 return self.errMsg()

if __name__ == '__main__':
	try:
	 bus = I2C(0)
	 print "Default I2C bus is accessible"
	except:
	 print "Error accessing default I2C bus"
