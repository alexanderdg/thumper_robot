from motorcontroller import Motorcontroller
import time

motor = Motorcontroller()
motor.timeout(1)
motor.forward(255)