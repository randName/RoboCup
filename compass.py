import smbus
import ctypes

class Compass:

	def __init__(self, bus, address, onebyte = True):
		self.bus = bus
		self.address = address
		self.onebyte = onebyte
		self.maxval = 256 if onebyte else 360.0

	def bearing(self):
		if self.onebyte:
			return self.bus.read_byte_data(self.address,1)
		else:
			
			b1 = self.bus.read_byte_data(self.address,2)
			b2 = self.bus.read_byte_data(self.address,3)
			return ((b1<<8)+b2)/10.0

	def zero(self):
		self.error = self.maxval - self.bearing()

	def pitch(self):
		return ctypes.c_byte(self.bus.read_byte_data(self.address,4)).value

	def roll(self):
		return ctypes.c_byte(self.bus.read_byte_data(self.address,5)).value

	def accelerometer(self):
		vals = []
		for x in range(3): 
			b1 = self.bus.read_byte_data(self.address,x*2+16)
			b2 = self.bus.read_byte_data(self.address,x*2+17)
			vals.append( ctypes.c_int16((b1<<8)+b2).value )
		return vals

	def read(self):
		return ( self.bearing() + self.error ) % self.maxval
