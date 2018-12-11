from Joystick import Joystick

class Decoder:
	def __init__(self):
		print "Create decoder class"
		self.joycalc = Joystick()
		self.joystick_VRX1 = 512
		self.joystick_VRY1 = 512
		self.joystick_PB1 = 0
		self.joystick_VRX2 = 512
		self.joystick_VRY2 = 512
		self.joystick_PB2 = 0
		self.calcCRC = 0
		self.rcvCRC = 0
		self.status = 0

	def decode(self, rcvdata):
		self.status = 0
		try:
			if rcvdata != "":
				rcvdata_split = (rcvdata.split(':'))
				self.joystick_VRX1 = int(rcvdata_split[0])
				self.joystick_VRY1 = int(rcvdata_split[1])
				self.joystick_PB1 = int(rcvdata_split[2])
				self.joystick_VRX2 = int(rcvdata_split[3])
				self.joystick_VRY2 = int(rcvdata_split[4])
				self.joystick_PB2 = int(rcvdata_split[5])
				self.rcvCRC = int(rcvdata_split[6])
				self.joycalc.calculate(self.getJoystickVRX1(), self.getJoystickVRY1())
				self.calcCRC = self.joystick_VRX1 + self.joystick_VRY1 + self.joystick_PB1 + self.joystick_VRX2 + self.joystick_VRY2 + self.joystick_PB2
				self.status = 1

		except ValueError, e:
			print "JSON type error"

		except IndexError, e:
			print "Ontvangen data was het verkeerde formaat"

	def processData(self):
		print "nop"

	def checkCRC(self):
		check = 0
		if self.rcvCRC == self.calcCRC:
			check = 1
		else:
			print "CRC fout opgetreden!"
		return check

	def getStatus(self):
		return self.status

	def getJoystickVRX1(self):
		return self.joystick_VRX1

	def getJoystickVRY1(self):
		return self.joystick_VRY1

	def getJoyStickPB1(self):
		return self.joystick_PB1

	def getJoystickVRX2(self):
		return self.joystick_VRX2

	def getJoystickVRY2(self):
		return self.joystick_VRY2

	def getJoystickPB2(self):
		return self.joystick_PB2

	def getJoystickM1(self):
		return self.joycalc.getM1()

	def getJoystickM2(self):
		return self.joycalc.getM2()