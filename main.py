import threading
import time
import signal
from ADC import ADC
from motorcontroller import Motorcontroller
from OA import OA
from Display import Display
from Buzzer import Buzzer
from Decoder import Decoder
from xbee import Xbee
from Joystick import Joystick
#sudo nano /home/pi/.bashrc

lowbatteryvoltage = 7.3

keep_reading = 1

class Serialcom(threading.Thread):

	def __init__(self):
		threading.Thread.__init__(self)
		self.shutdown_flag = threading.Event()
		self.motor = Motorcontroller()
		self.buzzer = Buzzer()
		self.xbee = Xbee()
		self.decoder = Decoder()
		self.servo1 = 96
		self.servo2 = 75
		self.joycalc = Joystick()
		self.motor.setServo1(self.servo1)
		self.motor.setServo2(self.servo2)
		self.lastSavedTime = 0


	def run(self):
		print('Thread #%s started' % self.ident)
		self.motor.timeout(1)
		while not self.shutdown_flag.is_set():
			rcvdata = self.xbee.read()
			self.decoder.decode(rcvdata)
			self.motor.recalCommand()
			currenttime = time.time()
			if currenttime - self.lastSavedTime > 1.0:
				self.lastSavedTime = time.time()
				self.xbee.sendBat()
			if self.decoder.getStatus() and self.decoder.checkCRC():
				if self.decoder.getJoyStickPB1() == 0:
					self.motor.EmergyStop()
					self.buzzer.beep(300)

				elif self.decoder.getJoystickM1() > 248 and self.decoder.getJoystickM2() > 248:
					self.joycalc.calculateReg(255)
					self.motor.Motor1MC2(255 - self.joycalc.cor1)
					self.motor.Motor2MC2(255 - self.joycalc.cor2)

				elif (abs(self.decoder.getJoystickM1() - self.decoder.getJoystickM2()) <= 3) and (self.decoder.getJoystickM1() > 50):
					self.joycalc.calculateReg(self.decoder.getJoystickM1())
					self.motor.Motor1MC2(self.decoder.getJoystickM1() - self.joycalc.cor1)
					self.motor.Motor2MC2(self.decoder.getJoystickM1() - self.joycalc.cor2)
					#print "drive forward without full speed"
				else:
					self.motor.Motor1MC2(self.decoder.getJoystickM1())
					self.motor.Motor2MC2(self.decoder.getJoystickM2())
					#print "other speeds"

				if self.decoder.getJoystickPB2() == 0:
					self.servo1 = 96
					self.motor.setServo1(self.servo1)
					self.buzzer.beep(300)

				elif self.decoder.getJoystickVRX2() > 1000:
					if(self.servo1 > 0):
						self.servo1 = self.servo1 - 1
						self.motor.setServo1(self.servo1)
				elif self.decoder.getJoystickVRX2() < 24:
					if(self.servo1 < 180):
						self.servo1 = self.servo1 + 1
						self.motor.setServo1(self.servo1)

				if self.decoder.getJoystickPB2() == 0:
					self.servo2 = 75
					self.motor.setServo2(self.servo2)

				elif self.decoder.joystick_VRY2 > 1000:
					if(self.servo2 > 0):
						self.servo2 = self.servo2 - 1
						self.motor.setServo2(self.servo2)
				elif self.decoder.getJoystickVRY2() < 24:
					if(self.servo2 < 180):
						self.servo2 = self.servo2 + 1
						self.motor.setServo2(self.servo2)

			time.sleep(0.001)

		# ... Clean shutdown code here ...
		self.xbee.close()
		self.motor.close()
		print('Thread #%s stopped' % self.ident)



class Batterymonitor(threading.Thread):
	def __init__(self):
		threading.Thread.__init__(self)
		self.shutdown_flag = threading.Event()
		self.adc = ADC()

	def run(self):
		print('Thread #%s started' % self.ident)
		while not self.shutdown_flag.is_set():
			self.adc.updateLed()
			batteryvoltage = self.adc.readVoltage()
			batterycurrent = self.adc.readCurrent()
			print("Battery voltage: %.2fV" % batteryvoltage)
			print("Battery current: %.2fA" % batterycurrent)
			if batteryvoltage < lowbatteryvoltage:
				print("Low battery !!!!!")
			time.sleep(1)

		# ... Clean shutdown code here ...
		print('Thread #%s stopped' % self.ident)


class CollisionDetection(threading.Thread):
	def __init__(self):
		threading.Thread.__init__(self)
		self.shutdown_flag = threading.Event()
		self.OA = OA()
		self.OA.setSensitivity(10)

	def run(self):
		print('Thread #%s started' % self.ident)
		while not self.shutdown_flag.is_set():
			result = self.OA.algoritme()
			if result == 1:
				print ("Thumper robot heeft een botsing gedetecteerd")

		# ... Clean shutdown code here ...
		print('Thread #%s stopped' % self.ident)

class Displaythread(threading.Thread):
	def __init__(self):
		threading.Thread.__init__(self)
		self.shutdown_flag = threading.Event()
		self.display = Display()

	def run(self):
		print('Thread #%s started' % self.ident)
		old_time = time.time()
		menu = 1
		while not self.shutdown_flag.is_set():
			if(time.time() - old_time > 5.0):
				old_time = time.time()
				if menu == 0:
					menu = 1
				else:
					menu = 0
			if menu == 0:
				self.display.printBatStatus()
			elif menu == 1:
				self.display.printBatStatus()

		# ... Clean shutdown code here ...
		self.display.printCloseMessage()
		print('Thread #%s stopped' % self.ident)


class ServiceExit(Exception):
	pass


def service_shutdown(signum, frame):
	print('Caught signal %d' % signum)
	raise ServiceExit


def main():
	signal.signal(signal.SIGTERM, service_shutdown)
	signal.signal(signal.SIGINT, service_shutdown)

	print('Starting main program')
	try:
		j1 = Serialcom()
		j2 = Batterymonitor()
		j3 = CollisionDetection()
		j4 = Displaythread()
		j1.start()
		j2.start()
		j3.start()
		j4.start()
		while True:
			time.sleep(0.5)

	except ServiceExit:
		j1.shutdown_flag.set()
		j2.shutdown_flag.set()
		j3.shutdown_flag.set()
		j4.shutdown_flag.set()
		j1.join()
		j2.join()
		j3.join()
		j4.join()

	print('Exiting main program')

if __name__ == '__main__':
    main()