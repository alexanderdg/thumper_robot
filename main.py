import serial
import threading
import time
import signal
from ADC import ADC


lowbatteryvoltage = 7.3

ser = serial.Serial('/dev/ttyS0' , baudrate=115200, timeout=1)  # open serial port
keep_reading = 1


class Serialcom(threading.Thread):
	def __init__(self):
		threading.Thread.__init__(self)
		self.shutdown_flag = threading.Event()

	def run(self):
		print('Thread #%s started' % self.ident)

		while not self.shutdown_flag.is_set():
			ser.write("testazz")
			rcvdata = ser.readline()
			if rcvdata != "":
				print rcvdata
			time.sleep(0.001)

		# ... Clean shutdown code here ...
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
			print("Battery voltage: %.2f" % batteryvoltage)
			if batteryvoltage < lowbatteryvoltage:
				print("Low battery !!!!!")
			time.sleep(10)

		# ... Clean shutdown code here ...
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
		j1.start()
		j2.start()
		while True:
			time.sleep(0.5)

	except ServiceExit:
		j1.shutdown_flag.set()
		j2.shutdown_flag.set()
		j1.join()
		j2.join()

	print('Exiting main program')

if __name__ == '__main__':
    main()