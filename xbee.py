import time
import serial

class Xbee:

	print ("Open xbee communication")
	def __init__(self, default=0):
		self.ser = serial.Serial(port='/dev/xbee',
		                         baudrate=115200,
		                         parity=serial.PARITY_NONE,
		                         stopbits=serial.STOPBITS_ONE,
		                         bytesize=serial.EIGHTBITS,
		                         timeout=1
		                         )

	def write(self, data):
		self.ser.write(data)

	def read(self):
		rcvdata = self.ser.readline()
		print "readline: " + rcvdata
		return rcvdata

	def sendACK(self):
		self.ser.write("ACK")
		print "data is ACK"