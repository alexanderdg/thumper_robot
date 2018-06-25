from motorcontroller import Motorcontroller
from mysocket import Mysocket
import time

motor = Motorcontroller()
socket = Mysocket()
motor.timeout(0)
motor.Motor1MC1(0, 55)
time.sleep(1)
motor.Motor2MC1(0,55)
#time.sleep(5)
motor.stop()
socket.readyToConnect()
time.sleep(100)
motor.close()
socket.close()
