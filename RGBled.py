import time
import RPi.GPIO as IO

class RGBled:
	def __init__(self):
		IO.setwarnings(False)
		IO.setmode(IO.BCM)
		IO.setup(13, IO.OUT)
		self.red = IO.PWM(13, 100)
		self.red.start(0)
		IO.setup(6, IO.OUT)
		self.green = IO.PWM(6, 100)
		self.green.start(0)
		IO.setup(5, IO.OUT)
		self.blue = IO.PWM(5, 100)
		self.blue.start(0)
		print ("Starting to control RGB led")

	def set_red(self, red):
		self.red.ChangeDutyCycle(float(red))

	def set_green(self, green):
		self.green.ChangeDutyCycle(float(green))

	def set_blue(self, blue):
		self.blue.ChangeDutyCycle(float(blue))

	def __del__(self):
		print("Close the led control")