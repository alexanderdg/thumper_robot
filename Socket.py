from ADC import ADC
from motorcontroller import Motorcontroller
from RGBled import RGBled
import serial
import time
import threading
import json

def send_worker():
	while 1:
		data_to_send = {"batteryvoltage": 0, "batterycurrent": 30}
		data_to_send['batteryvoltage'] =adc.readVoltage()
		data_to_send['batterycurrent'] = adc.readCurrent()
		ser.write(json.dumps(data_to_send))
		time.sleep(0.5)

def receive_worker():
	while 1:
		rcvdata = ser.readline()
		print rcvdata
		try:
			parsed_json = json.loads(rcvdata)
			led.set_red(parsed_json['LEDred'])
			led.set_green(parsed_json['LEDgreen'])
			led.set_blue(parsed_json['LEDblue'])
			motor.MotorYawComp(parsed_json['MotorYaw'])
			if parsed_json['MotorMode'] == 0:
				motor.stop()
			elif parsed_json['MotorMode'] == 1:
				motor.forward(parsed_json['MotorSpeed'])
			elif parsed_json['MotorMode'] == 2:
				motor.reverse(parsed_json['MotorSpeed'])
			elif parsed_json['MotorMode'] == 3:
				motor.turnLeft(parsed_json['MotorSpeed'])
			elif parsed_json['MotorMode'] == 4:
				motor.turnRight(parsed_json['MotorSpeed'])
			elif parsed_json['MotorMode'] == 5:
				motor.EmergyStop();
			else:
				motor.stop()


		except ValueError, e:
			print "JSON type error"
		time.sleep(0.004)

adc = ADC()
led = RGBled()
motor = Motorcontroller()
ser = serial.Serial(port='/dev/ttyS0',
		                         baudrate=115200,
		                         parity=serial.PARITY_NONE,
		                         stopbits=serial.STOPBITS_ONE,
		                         bytesize=serial.EIGHTBITS,
		                         timeout=1
		                         )

try:
	sendthread = threading.Thread(target=send_worker)
	receivethread = threading.Thread(target=receive_worker)
	sendthread.start()
	receivethread.start()
except:
	print "Error: unable to start thread"

while 1:
	time.sleep(1)