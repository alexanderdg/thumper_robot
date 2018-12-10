import threading
import time
import RPi.GPIO as IO

class Buzzer:
	def __init__(self):
		IO.setwarnings(False)
		IO.setmode(IO.BCM)
		IO.setup(26, IO.OUT)
		self.already_beep = 0

	def setOn(self):
		IO.output(26, IO.HIGH)

	def setOff(self):
		IO.output(26, IO.LOW)

	def run(self, timebeep):
		if timebeep > 5000:
			timebeep = 5000
		self.setOn()
		time.sleep(timebeep/1000.0)
		self.setOff()
		self.already_beep = 0

	def beep(self, timebeep):
		if self.already_beep == 0:
			threading.Thread(target=self.run, args=(timebeep,)).start()
			self.already_beep = 1
