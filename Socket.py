# Echo server program
import sys
from ADC import ADC
from motorcontroller import Motorcontroller
from RGBled import RGBled
import socket
import time
import threading
import json

def send_worker():
    while 1:
        conn.send("%f" % adc.readVoltage())
        time.sleep(0.5)

def receive_worker():
    while 1:
        rcvdata = conn.recv(1024)
        if not rcvdata: break
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
        #splitdata = rcvdata.split(":")
        #if len(splitdata) == 3:
            #print splitdata[0]  # mkyong.com
            #print splitdata[1]  # 100
            #print splitdata[2]  # 2015-10-1
            #led.set_red(splitdata[0])
            #led.set_green(splitdata[1])
            #led.set_blue(splitdata[2])
        time.sleep(0.004)

HOST = 'thumper.local'               # Symbolic name meaning all available interfaces
PORT = 50007              # Arbitrary non-privileged port
s = None
for res in socket.getaddrinfo(HOST, PORT, socket.AF_UNSPEC,
                              socket.SOCK_STREAM, 0, socket.AI_PASSIVE):
    af, socktype, proto, canonname, sa = res
    try:
        s = socket.socket(af, socktype, proto)
    except socket.error as msg:
        s = None
        continue
    try:
        s.bind(sa)
        s.listen(1)
    except socket.error as msg:
        s.close()
        s = None
        continue
    break
if s is None:
    print 'could not open socket'
    sys.exit(1)
conn, addr = s.accept()
print 'Connected by', addr
s.setblocking(0)
adc = ADC()
led = RGBled()
motor = Motorcontroller()

try:
   sendthread = threading.Thread(target=send_worker)
   receivethread = threading.Thread(target=receive_worker)
   sendthread.start()
   receivethread.start()
except:
   print "Error: unable to start thread"

while 1:
    time.sleep(1)
conn.close()
