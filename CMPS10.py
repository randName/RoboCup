#!/usr/bin/python 
from i2c import I2C 

class CMPS10:

	def __init__(self, address, onebyte = True):
		self.i2c = I2C(address)
		self.onebyte = onebyte
		self.maxval = 256 if onebyte else 360.0

	def rawBearing(self):
		if self.onebyte:
			return self.i2c.read8(1)
		else:
			return self.i2c.read16(2)/10.0

	def zero(self):
		self.error = self.maxval - self.bearing()

	def bearing(self):
		return ( self.rawBearing() + self.error ) % self.maxval

	def pitch(self):
		return self.i2c.read8(4,True)

	def roll(self):
		return self.i2c.read8(5,True)

	def accelerometer(self):
		return [ self.i2c.read16(x*2+16,True) for x in range(3) ]

if __name__ == "__main__":
	c = CMPS10(0x60)
	print c.rawBearing()
