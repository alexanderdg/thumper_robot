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

	def sendBat(self, rfrating):
		data_to_send = "{0:.2f}:{1:.2f}:{2:3d}&".format(round(self.adc.readVoltage(), 2), round(self.adc.readCurrent(), 2), rfrating)
		self.write(data_to_send)