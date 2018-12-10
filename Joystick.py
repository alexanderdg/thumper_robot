import math

class Joystick:
	print("Open joystick calculator")

	def __init__(self):
		self.m1 = 0
		self.m2 = 0

	def close(self):
		print("Close joystick calculator")

	def valmap(self, value, istart, istop, ostart, ostop):
		return (ostart + (float(ostop - ostart) * (float(value - istart) / float(istop - istart))))

	def calculate(self, jx, jy):
		nJoyX = -self.valmap(jx, 0, 1023, -128, 127)
		nJoyY = self.valmap(jy, 0, 1023, -128, 127)
		nMotPremixL = 0.0
		nMotPremixR = 0.0
		fPivScale = 0.0
		m1 = 0
		m2 = 0
		if nJoyY >= 0:
			if nJoyX >= 0:
				nMotPremixL = 127.0
				nMotPremixR = 127.0 - nJoyX
			else:
				nMotPremixL = 127.0 + nJoyX
				nMotPremixR = 127.0
		else:
			if nJoyX >= 0:
				nMotPremixL = 127.0 - nJoyX
				nMotPremixR = 127.0
			else:
				nMotPremixL = 127.0
				nMotPremixR = 127.0 + nJoyX
		nMotPremixL = nMotPremixL * nJoyY / 128.0
		nMotPremixR = nMotPremixR * nJoyY / 128.0
		nPivSpeed = nJoyX
		if abs(nJoyY) > 40.0:
			fPivScale = 0.0
		else:
			fPivScale = (1.0 - abs(nJoyY) / 40.0)
		nMotMixL = (1.0 - fPivScale) * nMotPremixL + fPivScale * (nPivSpeed)
		nMotMixR = (1.0 - fPivScale) * nMotPremixR + fPivScale * (-nPivSpeed)
		snMotMixL = self.valmap(nMotMixL, -128, 127, -255, 255)
		snMotMixR = self.valmap(nMotMixR, -128, 127, -255, 255)
		if abs(snMotMixL) < 10:
			snMotMixL = 0
		if abs(snMotMixR) < 10:
			snMotMixR = 0
		if snMotMixL > 255:
			snMotMixL = 255
		if snMotMixR > 255:
			snMotMixR = 255
		if snMotMixL < -255:
			snMotMixL = -255
		if snMotMixR < -255:
			snMotMixR = -255
		self.m1 = int(snMotMixL)
		self.m2 = int(snMotMixR)

	def getM1(self):
		return self.m1

	def linToLog(self, lin):
		output = math.log1p(lin + 1) / math.log1p(256) * 256
		return output

	def getM2(self):
		return self.m2