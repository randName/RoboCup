import smbus

class Compass:

	def __init__(self, bus, address, onebyte = True):
		self.bus = bus
		self.address = address
		self.onebyte = onebyte
		self.maxval = 255 if onebyte else 3599

	def bearing(self):
		if self.onebyte:
			return self.bus.read_byte_data(self.address, 1)
		else:
			
			b1 = self.bus.read_byte_data(self.address, 2)
			b2 = self.bus.read_byte_data(self.address, 3)
			return ( b1 << 8 ) + b2

	def zero(self):
		self.error = self.maxval - self.bearing(self.onebyte)

	def pitch(self):
		return self.bus.read_byte_data(self.address, 4)

	def roll(self):
		return self.bus.read_byte_data(self.address, 5)

	def read(self):
		return self.bearing() + self.error
