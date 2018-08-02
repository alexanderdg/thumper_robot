from motorcontroller import Motorcontroller
import time

motor = Motorcontroller()
motor.timeout(0)
motor.forward(0, 255)