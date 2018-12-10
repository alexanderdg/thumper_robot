import serial
import threading
import time
import signal
import json
from ADC import ADC
from motorcontroller import Motorcontroller
from OA import OA
from Display import Display
from Joystick import Joystick
from Buzzer import Buzzer
#sudo nano /home/pi/.bashrc

lowbatteryvoltage = 7.3

keep_reading = 1



class Serialcom(threading.Thread):
	cor2 = 0
	cor1 = 0

	def __init__(self):
		threading.Thread.__init__(self)
		self.shutdown_flag = threading.Event()
		self.motor = Motorcontroller()
		self.buzzer = Buzzer()
		self.ser = serial.Serial('/dev/ttyS0', baudrate=115200, timeout=1)  # open serial port
		self.adc = ADC()
		self.joycalc = Joystick()
		self.servo1 = 96
		self.servo2 = 75
		self.motor.setServo1(self.servo1)
		self.motor.setServo2(self.servo2)
		self.lastSavedTime = 0

	def calculateReg(self, level):
		regression = (int)((0.0008009 * pow(level, 2)) + (-0.171963 * level) - 0.7819);
		if (regression >= 0) :
			self.cor1 = 0
			self.cor2 = regression
		else:
			self.cor1 = -regression
			self.cor2 = 0
		return regression



	def run(self):
		print('Thread #%s started' % self.ident)
		self.motor.timeout(1)
		while not self.shutdown_flag.is_set():
			rcvdata = self.ser.readline()
			self.motor.recalCommand()
			currenttime = time.time()
			if currenttime - self.lastSavedTime > 1.0:
				self.lastSavedTime = time.time()
				data_to_send = "{0}V {1}A&".format(str(round(self.adc.readVoltage(),2)), str(round(self.adc.readCurrent(),2)))
				self.ser.write(data_to_send)
			if rcvdata != "":
				try:
					rcvdata_split = (rcvdata.split(':'))
					#print rcvdata_split
					rcv1 = int(rcvdata_split[0])
					rcv2 = int(rcvdata_split[1])
					rcv3 = int(rcvdata_split[3])
					rcv4 = int(rcvdata_split[4])
					self.joycalc.calculate(rcv1, rcv2)
					inttemp1 = self.joycalc.getM1()
					inttemp2 = self.joycalc.getM2()
					if rcvdata_split[2] == "0":
						self.motor.EmergyStop()
						self.buzzer.beep(300)

					elif inttemp1 > 248 and inttemp2 > 248:
						self.calculateReg(255)
						self.motor.Motor1MC2(255 - 0)
						self.motor.Motor2MC2(255 - 7)
						#print "cor1: {}", format(255 - self.cor1)
						#print "cor2: {}", format(255 - self.cor2)
						#print "ride forward with full speed"

					elif (abs(inttemp1 - inttemp2) <= 3) and (inttemp1 > 50):
						self.calculateReg(inttemp1)
						self.motor.Motor1MC2(inttemp1 - self.cor1)
						self.motor.Motor2MC2(inttemp1 - self.cor2)
						#print "drive forward without full speed"
					else:
						self.motor.Motor1MC2(inttemp1)
						self.motor.Motor2MC2(inttemp2)
						#print "other speeds"

					if rcvdata_split[5] == "0":
						self.servo1 = 96
						self.motor.setServo1(self.servo1)
						self.buzzer.beep(300)

					elif rcv3 > 1000:
						if(self.servo1 > 0):
							self.servo1 = self.servo1 - 1
							self.motor.setServo1(self.servo1)
					elif rcv3 < 24:
						if(self.servo1 < 180):
							self.servo1 = self.servo1 + 1
							self.motor.setServo1(self.servo1)

					if rcvdata_split[5] == "0":
						self.servo2 = 75
						self.motor.setServo2(self.servo2)

					elif rcv4 > 1000:
						if(self.servo2 > 0):
							self.servo2 = self.servo2 - 1
							self.motor.setServo2(self.servo2)
					elif rcv4 < 24:
						if(self.servo2 < 180):
							self.servo2 = self.servo2 + 1
							self.motor.setServo2(self.servo2)

				except ValueError, e:
					print "JSON type error"

				except IndexError, e:
					print "Ontvangen data was het verkeerde formaat"
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
