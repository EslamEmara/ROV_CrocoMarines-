from DcControl import addDCMotor
from Directions import Direction
from CameraControl import camera 
from ServoControl import Servo
import time
CurrentDirection=""
class Control:
    def __init__(self):
       self.rov=Direction()                             #object from the directions class
       self.cam = camera()                              #object from the camera control class
       self.servoforgripper = Servo()                   #object for main gripper direction class
       self.DC=addDCMotor(14,15)                        #object for Dc motor class
       self.MicroDC=addDCMotor(20,21)                   #dc motor for micro gripper
       self.MicroMotor=addDCMotor(17,27)                #motor for micro rov motion
       return
    def MainROV(self,msg):
        array = msg.split()
        global CurrentDirection
##############################################################################################################
######## as no speed is given (addition speed =0) the rov motors will operate with its mininmum speed#########
##############################################################################################################
        if(array[0]=="move"):
            if(array[1]=="forward"):                   #forward
               self.rov.forward(0)
               CurrentDirection="forward"
            
            elif(array[1]=="backward"):                #backward
                self.rov.Backward(0)
                CurrentDirection = "backward"
            
            elif(array[1]=="right"):                   #slide right
                self.rov.Right(0)
                CurrentDirection = "right"
           
            elif(array[1]=="left"):                    #slide left
                self.rov.Left(0)
                CurrentDirection = "left"
            
            elif(array[1]=="up"):                      #upward
                self.rov.Up(0)
                CurrentDirection = "up"
            
            elif(array[1]=="down"):                    #downward
                self.rov.Down(0)
                CurrentDirection = "down"

            elif(array[1]=="rolltoright"):             #rolling clockwise
                self.rov.RollToRight(0)
                CurrentDirection = "rolltoright"

            elif(array[1]=="rolltoleft"):              #rolling counterclockwise
                self.rov.RollToLeft(0)
                CurrentDirection = "rolltoleft"    
            
            elif(array[1]=="pitchup"):                 #pitching up
                self.rov.PitchUp(0)
                CurrentDirection = "pitchup"

            elif(array[1]=="pitchdown"):               #pitching down
                self.rov.PitchDown(0)
                CurrentDirection = "pitchdown"

            elif(array[1]=="yawcw"):                   #rotating right 
                self.rov.YawCw(0)
                CurrentDirection = "yawcw"

            elif(array[1]=="yawccw"):                  #rotating left 
                self.rov.YawCCw(0)
                CurrentDirection = "yawccw"
            elif(array[1]== "stop"):
                self.rov.Stop()                       #motors stopped
#####################################################################################################################################
## as speed will be given now (addition speed >0)the motors will operate with speed equals their minimum speed plus the added speed##
#####################################################################################################################################
        
        elif(array[0]=="speed"):
            if (CurrentDirection == "forward"):
                self.rov.forward(int(array[1]))
            elif (CurrentDirection == "backward"):
                self.rov.Backward(int(array[1]))
            elif (CurrentDirection == "right"):
                self.rov.Right(int(array[1]))
            elif (CurrentDirection == "left"):
                self.rov.Left(int(array[1]))
            elif (CurrentDirection == "up"):
                self.rov.Up(int(array[1]))   
            elif (CurrentDirection == "down"):
                self.rov.Down(int(array[1])) 
            elif (CurrentDirection == "rolltoright"):
                self.rov.RollToRight(int(array[1]))
            elif (CurrentDirection == "rolltoleft"):
                self.rov.RollToLeft(int(array[1]))
            elif (CurrentDirection == "pitchup"):
                self.rov.PitchUp(int(array[1]))
            elif (CurrentDirection == "pitchdown"):
                self.rov.PitchDown(int(array[1]))    
            elif (CurrentDirection == "yawcw"):
                self.rov.YawCw(int(array[1]))
            elif (CurrentDirection == "yawccw"):
                self.rov.YawCCw(int(array[1]))  

###########################################################################################################################################
#########################################################  servo cam part    ##############################################################
###########################################################################################################################################    
        
        elif(array[0]=="cam"):
            
            if(array[1]=="up"):                  #raising camera up
               self.cam.camup()
            
            elif(array[1]=="down"):              #lowering camera down
                self.cam.camdown()

###########################################################################################################################################
#########################################################  main grippers's servo ###########################################################
###########################################################################################################################################

        elif(array[0]=="sgrip"):
            
            if(array[1]=="r"):                  #gripper moves right
               self.servoforgripper.Right()
            elif(array[1]=="l"):                #grippers moves left
                self.servoforgripper.left()  
            elif(array[1]=="n"):                #grippers moves to middle  
                self.servoforgripper.Neutral()

###########################################################################################################################################
#########################################################  main grippers's switch ###########################################################
###########################################################################################################################################

        elif (array[0] == "grip"):
            if (array[1] == "close"):                # gripper close
                self.DC.Run()
                self.DC.forward()
            elif (array[1] == "open"):               # grippers open
                self.DC.Run()
                self.DC.Backward()
            elif (array[1]=="hold"):                 #gripper hold at its position
                self.DC.stop()    
###############################################################################################################################################
###############################################################################################################################################
###############################################################################################################################################
###############################################################################################################################################
###############################################################################################################################################

    def MicroROV (self,msg):
        array = msg.split()
        if (array[0] == "micro"):
            if (array[1] == "forward"):                            #micro rov goes forward
                self.MicroMotor.Run()
                self.MicroMotor.forward()
            elif (array[1] == "backward"):                         #micro rov goes backward                                       
                self.MicroMotor.Run()
                self.MicroMotor.Backward()
            elif  (array[1] == "stop"):                            #micro rov stops
                self.MicroMotor.stop()             
            elif (array[1] == "close"):                            # micro rov gripper close
                self.MicroDC.Run()
                self.MicroDC.forward()
            elif (array[1] == "open"):                             # micro rov gripper open
                self.MicroDC.Run()
                self.MicroDC.Backward()
            elif (array[1] == "hold" ):                             #holds the gripper position      
                self.MicroDC.stop()   
