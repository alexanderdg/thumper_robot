import serial
from ADC import ADC

class Xbee:

	print ("Open xbee communication")
	def __init__(self, default=0):
		self.ser = serial.Serial('/dev/ttyS0', baudrate=115200, timeout=1)  # open serial port
		self.adc = ADC()

	def write(self, data):
		self.ser.write(data)

	def read(self):
		rcvdata = self.ser.readline()
		return rcvdata

	def sendACK(self):
		self.ser.write("ACK")

	def close(self):
		self.ser.close()

	def sendBat(self):
		data_to_send = "{0}V {1}A&".format(str(round(self.adc.readVoltage(), 2)), str(round(self.adc.readCurrent(), 2)))
		self.write(data_to_send)