

import  RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.Board)
class Servo:
    def __init__(self):
        self.pin = 13
        print("servo is intailised with speed zero at pin :", self.pin)
        self.p=GPIO.PWM(self.pin,50)
        self.p.start(7.5)
        time.sleep(0.5)
        return
    def Right(self):
        self.p.changeDutyCycle(2.5)
        print("servo move to right")
        time.sleep(1)
        return

    def left(self):
        self.p.changeDutyCycle(12.5)
        print("servo move to left")
        time.sleep(1)
        return

    def Neutral (self):
        self.p.changeDutyCycle(7.5)
        print("servo move to north")
        time.sleep(1)
        return