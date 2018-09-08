import time
from threading import Thread
from mpu6050 import mpu6050
from RGBled import RGBled

class OA:
	def __init__(self):
		print ("Creating Obstacle avoidance algoritme")
		self.mpu = mpu6050(0x68)
		self.led = RGBled()
		self.led.set_red(0)
		self.sensitivity = 10

	def start(self):
		print ("Starting Obstacle avoidance algoritme")
		self.thread_run = True
		self.my_thread = Thread(target=self.algoritme())
		self.my_thread.setDaemon(True)
		self.my_thread.start()

	def algoritme(self):
		while self.thread_run:
			accldata = self.mpu.get_accel_data()
			xaccl = accldata['x']
			print xaccl
			if abs(xaccl) > self.sensitivity:
				time.sleep(0.03)
				if xaccl > self.sensitivity:
					self.led.set_red(100)
					time.sleep(2)
					self.led.set_red(0)
			time.sleep(0.1)

if __name__ == '__main__':
	oa = OA()
	oa.start()