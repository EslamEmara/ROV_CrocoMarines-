import  RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.Board)

class addDCMotor:
    def __init__(self,pin1,pin2):                  # one for Dc pwm, and another for direction
        self.pins=[pin1,pin2]
       for i in range (2):
           GPIO.setup(self.pins[i], GPIO.OUT)
           print("set the mode of pins", self.pins[i])
       self.pwm=GPIO.PWM(pins[0],100)
       self.pwm.start(0)
       time.sleep(0.5)

    def Run(self):  #run the motor
        self.pwm.ChangeDutyCycle(50)    #medium speed
        print("the DC motor at pin :", self.pins[0], "is Run ")
        time.sleep(1)
        return
    def stop(self):  # stopping the motor
        self.pwm.ChangeDutyCycle(0)
        print("the DC motor at pin :", self.pins[0], "is stopped ")
        time.sleep(1)
        return
    def forward(self): #for forward macro direction..
        GPIO.output(self.pins[1], 1)
        print("the DC motor at pin :", self.pins[1], "move forward ")
        time.sleep(1)
        return

    def Backward(self): #for Backward macro direction..
        GPIO.output(self.pins[1], 0)
        print("the DC motor at pin :", self.pins[1], "move backward ")
        time.sleep(1)
        return
