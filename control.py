##############################################
###### we use another library here ###########
##############################################
import RPi.GPIO as GPIO
import time

camera_pos=7
class camera :
#servo motors operate from duty cycle 2 for 0 degree to duty cycle 12 for 180 degree
#duty cycle 0 turns the servo off
#we intialize the servo with duty cycle 7 to make it horizontally 90 degree then we can either increase it to 180 or decrease it to 0 degree
    def __init__ (self) :
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(11,GPIO.OUT)
        servo = GPIO.PWM(11,50)                                  #intializing the servo with frequency 50hz and duty cycle 0 "stopped"
        servo.start(0)
    def camup(self):
        global camera_pos
        if camera_pos <12 :
            servo.ChangeDutyCycle(camera_pos)                    #increasing the duty cycle of servo to raise the camera up
            time.sleep(0.5)
            print("camera is up to position ",camera_pos)
            camera_pos+=1
            servo.ChangeDutyCycle(0)                             #after setting the servo in required position we turn it off to 
            time.sleep(0.2)                                      #eliminate the jitter effect
        else :
            pass

    def camdown (self):
        global camera_pos
        if camera_pos>=2 :
            servo.ChangeDutyCycle(camera_pos)                   #decreasing the duty cycle of servo to lower the camera down
            time.sleep(0.5)
            print("camera is down to position ",camera_pos)
            camera_pos-=1
            servo.ChangeDutyCycle(0)                            #after setting the servo in required position we turn it off to
            time.sleep(0.2)                                     #eliminate the jitter effect



