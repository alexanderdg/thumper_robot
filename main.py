from motorcontroller import Motorcontroller
import time

motor = Motorcontroller()
motor.timeout(0)
motor.Motor1MC1(0, 255)
time.sleep(1)
motor.Motor2MC1(0,255)
#time.sleep(5)
motor.stop()
time.sleep(1)
motor.close()
