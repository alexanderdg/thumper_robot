from mcp3204 import MCP3208
from RGBled import RGBled
import time

class ADC:
	def __init__(self):
		print ("Starting Current en voltage measurments")
		self.spi = MCP3208(0)
		self.rgb = RGBled()
		self.intRes = 0.0420

	def __del__(self):
		self.close

	def readCurrent(self):
		a1 = 0
		for x in range(0,10):
			a1 += self.spi.read(1)
		current = (((a1/10)-1946)/41.1)
		#print "current=%f" % current
		return current

	def readVoltage(self):
		batterycurrent = self.readCurrent()
		dropout = (batterycurrent * batterycurrent) * self.intRes
		a0 = 0
		for x in range(0,10):
			a0 += self.spi.read(0)
		voltage = ((a0/10)/218.66)
		#voltage += dropout
		#print "voltage=%f" % voltage
		return voltage

	def updateLed(self):
		batteryvoltage = self.readVoltage()
		batterycurrent = self.readCurrent()
		dropout = (batterycurrent * batterycurrent) * self.intRes
		if batteryvoltage > 8.6:
			self.rgb.set_red(0)
			self.rgb.set_green(100)
		elif batteryvoltage < 7.1:
			self.rgb.set_red(100)
			self.rgb.set_green(0)
		else:
			temp = batteryvoltage - 7.1
			temp2 = (int)((temp / 1.5) * 100)
			self.rgb.set_green(temp2)
			self.rgb.set_red(100 - temp2)

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