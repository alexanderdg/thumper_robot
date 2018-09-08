import time
from threading import Thread
from mpu6050 import mpu6050
from RGBled import RGBled

class OA:
	def __init__(self):
		print ("Creating Obstacle avoidance algoritme")
		self.mpu = mpu6050(0x68)
		self.sensitivity = 10

	def setSensitivity(self, sensitivity):
		self.sensitivity = sensitivity

	def algoritme(self):
		accldata = self.mpu.get_accel_data()
		xaccl = accldata['x']
		collision = 0
		if abs(xaccl) > self.sensitivity:
			time.sleep(0.03)
			if xaccl > self.sensitivity:
				collision = 1
		time.sleep(0.01)
		return collision

if __name__ == '__main__':
	oa = OA()
	oa.start()