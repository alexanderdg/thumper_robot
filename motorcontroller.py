import serial
import time
from threading import Thread




class Motorcontroller:
	print ("Open serial communication")
	print ("Succeeded to open serial communication")

	def __init__(self, default=0):
		self.ser=serial.Serial(port='/dev/motorcontroller',
		                       baudrate=115200,
		                       parity=serial.PARITY_NONE,
		                       stopbits=serial.STOPBITS_ONE,
		                       bytesize=serial.EIGHTBITS,
		                       timeout=1
		                       )
		self.keep_reading = True
		self.my_thread = Thread(target=self.print_serial_output)
		self.my_thread.setDaemon(True)
		self.my_thread.start()
		self.print_serial = True
		self.lastValueC9 = 0
		self.lastValueC10 = 0
		self.lastMotorCom = 0
		self.lastTimeComExc = 0
		self.recall = 0
		self.setServo1(96)
		self.setServo2(75)
		print ("init method")

	def close(self):
		if self.my_thread.is_alive():
			self.keep_reading = False
			self.my_thread.join()
		self.ser.close()
		print ("close motorcontroller")


	def print_serial_output(self):
		while self.keep_reading and self.ser.isOpen:
			#data = self.ser.readline()


			time.sleep(0.001)

	def stop(self):
		data_to_send = "0\n"
		self.ser.write(data_to_send)
		self.lastMotorCom = 0
		self.lastTimeComExc = time.time()

	def forward(self, speed):
		print("write to forward")
		data_to_send = "1:{0}\n".format(str(speed))
		self.ser.write(data_to_send)
		self.lastMotorCom = 1
		self.lastTimeComExc = time.time()

	def reverse(self, speed):
		data_to_send = "2:{0}\n".format(str(speed))
		self.ser.write(data_to_send)
		self.lastMotorCom = 2
		self.lastTimeComExc = time.time()

	def turnRight(self, speed):
		data_to_send = "3:{0}\n".format(str(speed))
		self.ser.write(data_to_send)
		self.lastMotorCom = 3
		self.lastTimeComExc = time.time()

	def turnLeft(self, speed):
		data_to_send = "4:{0}\n".format(str(speed))
		self.ser.write(data_to_send)
		self.lastMotorCom = 4
		self.lastTimeComExc = time.time()

	def acceleration(self, acceleration):
		data_to_send = "5:{0}\n".format(str(acceleration))
		self.ser.write(data_to_send)

	def timeout(self, timeout):
		data_to_send = "6:{0}\n".format(str(timeout))
		self.ser.write(data_to_send)

	def Motor1MC1(self, direction, speed):
		data_to_send = "7:{0}:{1}\n".format(str(direction), str(speed))
		self.ser.write(data_to_send)
		self.lastMotorCom = 7
		self.lastTimeComExc = time.time()

	def Motor2MC1(self, direction, speed):
		data_to_send = "8:{0}:{1}\n".format(str(direction), str(speed))
		self.ser.write(data_to_send)
		self.lastMotorCom = 8
		self.lastTimeComExc = time.time()

	def Motor1MC2(self, speed):
		if(self.lastValueC9 != speed or self.recall == 1):
			data_to_send = "9:{0}\n".format(str(speed))
			self.lastValueC9 = speed
			self.ser.write(data_to_send)
			self.lastMotorCom = 9
			self.lastTimeComExc = time.time()
			self.recall = 0

	def Motor2MC2(self, speed):
		if(self.lastValueC10 != speed or self.recall == 1):
			data_to_send = "10:{0}\n".format(str(speed))
			self.lastValueC10 = speed
			self.ser.write(data_to_send)
			self.lastMotorCom = 10
			self.lastTimeComExc = time.time()
			self.recall = 10

	def MotorYawComp(self, compensation):
		data_to_send = "11:{0}\n".format(str(compensation))
		self.ser.write(data_to_send)

	def EmergyStop(self):
		if self.lastMotorCom != 12:
			data_to_send = "12:0\n"
			self.ser.write(data_to_send)
			self.lastMotorCom = 12
			self.lastTimeComExc = time.time()

	def UnsafeEmergyStop(self):
		data_to_send = "13\n"
		self.ser.write(data_to_send)

	def setLoggingOff(self):
		self.print_serial = False

	def setLoggingOn(self):
		self.print_serial = True

	def setServo1(self, pos):
		if pos >= 0 and pos <= 180:
			data_to_send = "14:{0}\n".format(str(pos))
			self.ser.write(data_to_send)

	def setServo2(self, pos):
		if pos >= 0 and pos <= 180:
			data_to_send = "15:{0}\n".format(str(pos))
			self.ser.write(data_to_send)

	def recalCommand(self):
		currenttime = time.time()
		if (currenttime - self.lastTimeComExc) > 0.6:
			if self.lastMotorCom == 9 and self.lastValueC9 != 0:
				print "recall for command 9"
				self.Motor1MC2(self.lastValueC9)
				self.recall = 1
			elif self.lastMotorCom == 10 and self.lastValueC10 != 0:
				print "recall for command 10"
				self.Motor2MC2(self.lastValueC10)
				self.recall = 1

if __name__ == "__main__":
	print "motortest"
	motorcontroller = Motorcontroller()
	time.sleep(2)
	motorcontroller.forward(150)
	time.sleep(1)
	motorcontroller.stop()