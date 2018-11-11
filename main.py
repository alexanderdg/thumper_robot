import serial
import threading
import time
import signal
import json
from ADC import ADC
from motorcontroller import Motorcontroller
from OA import OA
from Display import Display
#sudo nano /home/pi/.bashrc

lowbatteryvoltage = 7.3

keep_reading = 1


class Serialcom(threading.Thread):
	def __init__(self):
		threading.Thread.__init__(self)
		self.shutdown_flag = threading.Event()
		self.motor = Motorcontroller()
		self.ser = serial.Serial('/dev/ttyS0', baudrate=115200, timeout=1)  # open serial port

	def run(self):
		print('Thread #%s started' % self.ident)
		self.motor.timeout(1)
		while not self.shutdown_flag.is_set():
			rcvdata = self.ser.readline()
			if rcvdata != "":
				try:
					parsed_json = json.loads(rcvdata)
					self.motor.MotorYawComp(parsed_json['MotorYaw'])
					if parsed_json['MotorMode'] == 0:
						self.motor.stop()
					elif parsed_json['MotorMode'] == 1:
						self.motor.forward(parsed_json['MotorSpeed'])
					elif parsed_json['MotorMode'] == 2:
						self.motor.reverse(parsed_json['MotorSpeed'])
					elif parsed_json['MotorMode'] == 3:
						self.motor.turnLeft(parsed_json['MotorSpeed'])
					elif parsed_json['MotorMode'] == 4:
						self.motor.turnRight(parsed_json['MotorSpeed'])
					elif parsed_json['MotorMode'] == 5:
						self.motor.EmergyStop();
					else:
						self.motor.stop()


				except ValueError, e:
					print "JSON type error"
			time.sleep(0.001)

		# ... Clean shutdown code here ...
		self.ser.close()
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
			time.sleep(10)

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
				self.display.printDaignosctic()

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
