from mcp3204 import MCP3208
import time

class ADC:
	def __init__(self):
		print ("Starting Current en voltage measurments")
		self.spi = MCP3208(0)

	def __del__(self):
		self.close

	def readCurrent(self):
		a1 = 0
		for x in range(0,10):
			a1 += self.spi.read(1)
		current = (((a1/10)-1902)/64.3)
		print "current=%f" % current
		return current

	def readVoltage(self):
		a0 = 0
		for x in range(0,10):
			a0 += self.spi.read(0)
		voltage = ((a0/10)/218.66)
		print "voltage=%f" % voltage
		return voltage

	def close(self):
		if self.conn != None:
			self.conn.close
			self.conn = None

if __name__ == '__main__':
	ADC_local = ADC()
	while True:
		ADC_local.readCurrent()
		ADC_local.readVoltage()
		time.sleep(0.010)