#import  RPi.GPIO as GPIO
import time

from ServoControl import Servo
#GPIO.setmode(GPIO.BOARD)
pins = [3,5,7]   #the pins for servo for glapper
class Direction :
    def __init__(self):
        for i in range(8) :
          # GPIO.setup(pins[i], GPIO.OUT)
          print("set the mode of pins",pins[i])
        self.Gripper1 = Servo(pins[0])
        self.Gripper2 = Servo(pins[1])
        self.Gripper3 = Servo(pins[2])
        time.sleep(7)
        print("servos are ready >>>")
        return
    def MotionGripper (self,msg):
        # .......
      return