

#import  RPi.GPIO as GPIO
import time

class Servo:
    def __init__(self, gpiopin):
        self.pin = gpiopin
        print("servo is intailised with speed zero at pin :", self.pin)
        #self.p=GPIO.PWM(self.pin,50)
        #self.p.start(7.5)
        return
    def Right(self):
        #self.p.changeDutyCycle(2.5)
        print("servo move to right")
        return

    def left(self):
        #self.p.changeDutyCycle(12.5)
        print("servo move to left")
        return

    def Neutral (self):
        #self.p.changeDutyCycle(7.5)
        print("servo move to north")
        return