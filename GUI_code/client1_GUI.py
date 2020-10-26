import time
import socket
import threading
import pygame
from pygame.locals import*
import sys
import select

import PyQt5
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUiType
from PyQt5 import QtCore
from PyQt5.QtCore import QCoreApplication

#import os#
import os
from os import path

FORM_CLASS, _ = loadUiType(path.join(path.dirname(__file__), "client1.ui"))

class MainApp(QMainWindow , FORM_CLASS):
    def __init__(self, msg, parent=None):
        super(MainApp , self).__init__(parent)
        QMainWindow.__init__(self)
        # self.PORT = 8000
        self.FORMAT = 'utf-8'
        self.DISCONNECT_MSG = "!DISCONNECT"
        # self.IP = socket.gethostbyname(socket.gethostname())
        # self.ADDR = (self.IP,self.PORT)
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        pygame.init()
        #self.screen = pygame.display.set_mode((640,480))
        #pygame.display.set_caption("Joystick Testing")
        #pygame.display.iconify()

        self.joystick_count = pygame.joystick.get_count()
        print("Number of joysticks:",format(self.joystick_count) )

        for i in range(self.joystick_count):
            self.joystick = pygame.joystick.Joystick(i)
            self.joystick.init()
            print("initialized joystick",i)

        self.speed = 0
        self.RUN = True
        self.msg = msg
        self.connected = False
        self.sr = False         #slide right flag
        self.sl = False         #slide left flag
        self.mu = False         #move up flag
        self.md = False         #move down flag
        self.pu = False         #pitch up flag
        self.pd = False         #pitch down flag
        self.rolr = False       #roll right flag
        self.roll = False       #roll left flag
        self.rotr = False       #rotate right flag
        self.rotl = False       #rotate left flag

        #thread_01 = threading.Thread(target=self.send_msg)
        thread_02 = threading.Thread(target = self.receive, args=())
        
        #thread_01.start()
        thread_02.start()

        self.setupUi(self)
        self.Handel_UI()
        self.Handel_Buttons()


    def Handel_UI(self):
        self.setWindowTitle('GUI test')
        self.setFixedSize(747, 430)

        self.lineEdit_2.setMaxLength(5)
        self.lineEdit.setMaxLength(13)
        self.lineEdit_2.setValidator(QIntValidator())
        #self.lineEdit.setValidator(QIntValidator())


    def Handel_Buttons(self):
        self.pushButton.clicked.connect(self.start)
        self.pushButton_2.clicked.connect(self.Disconnect)

    def Disconnect(self):
        if self.connected:
            self.msg = "[DISCONNECTING] Disconnecting Client."
            self.server.send(self.msg.encode(self.FORMAT))
            time.sleep(0.15)
            self.server.close()
            self.label_14.setText("Disconnected")
            self.label_19.setText("Static")
            self.label_4.setText("")
            self.label_9.setText("")
            self.label_8.setText("")
            self.label_5.setText("")
            self.label_7.setText("")
            self.label_6.setText("")
        else:
            pass
        

    def start(self):
        try:
            
            PORT = self.lineEdit_2.text()
            PORT = int(PORT)
            IP = self.lineEdit.text()
            ADDR = (IP, PORT)

            self.server.connect(ADDR)
            print(f"[CONNECTION] successfully connected to {ADDR} \n")
            self.connected = True
        except:
            pass

        if self.connected == True:
            self.label_14.setText("Connected")
            self.lineEdit_2.setReadOnly(True)
            self.lineEdit.setReadOnly(True)
            


###################################################################################################
###################################################################################################
    def send_msg(self):
        # global RUN
        # global speed
        for event in pygame.event.get():

            # if event.type == pygame.QUIT:
            #     print ("Received event 'Quit', exiting.")
            #     #sys.exit()
            #     self.RUN = False
            #     break

            # if event.type == KEYDOWN and event.key == K_ESCAPE :
            #     print ("Escape key pressed, exiting.")
            #     #sys.exit()
            #     self.RUN = False
            #     break


            if event.type == JOYBUTTONDOWN:

                if event.button == 0 and event.joy == 0:        
                    print("button 0 is pressed on controller 0")
                    self.msg = "button 0 is pressed on controller 0"
                    self.server.send(self.msg.encode(self.FORMAT))
                    time.sleep(0.15)

                if event.button == 1 and event.joy == 0:
                    print("button 1 is pressed on controller 0")
                    self.msg = "button 1 is pressed on controller 0"
                    self.server.send(self.msg.encode(self.FORMAT))
                    time.sleep(0.15)

                if event.button == 2 and event.joy == 0:        
                    print("button 2 is pressed on controller 0")
                    self.msg = "button 2 is pressed on controller 0"
                    self.server.send(self.msg.encode(self.FORMAT))
                    time.sleep(0.15)

                if event.button == 3 and event.joy == 0:
                    print("button 3 is pressed on controller 0")
                    self.msg = "button 3 is pressed on controller 0"
                    self.server.send(self.msg.encode(self.FORMAT))
                    time.sleep(0.15)

                if event.button == 4 and event.joy == 0:
                    print("button 4 is pressed on controller 0")
                    self.msg = "button 4 is pressed on controller 0"
                    self.server.send(self.msg.encode(self.FORMAT))
                    time.sleep(0.15)

                if event.button == 5 and event.joy == 0:
                    print("button 5 is pressed on controller 0")
                    self.msg = "button 5 is pressed on controller 0"
                    self.server.send(self.msg.encode(self.FORMAT))
                    time.sleep(0.15)

                if event.button == 6 and event.joy == 0:            #speed down
                    #print("button 6 is pressed on controller 0")
                    self.speed = self.speed - 30
                    #print("speed decreased by 30, new value:",speed+1500)
                    if self.speed <= 0 :
                        self.speed = 0
                    self.msg = "speed " + str(self.speed)
                    print(self.msg)
                    self.server.send(self.msg.encode(self.FORMAT))
                    self.label_4.setText(str(self.speed))
                    time.sleep(0.15)
                    

                if event.button == 7 and event.joy == 0:                #speed up                
                    #print("button 7 is pressed on controller 0")
                    self.speed = self.speed +30
                    #print("speed increased by 30, new value:",speed+1500)
                    if self.speed >= 400 :
                        self.speed = 400
                    self.msg = "speed " + str(self.speed)
                    print(self.msg)
                    self.server.send(self.msg.encode(self.FORMAT))
                    self.label_4.setText(str(self.speed))
                    time.sleep(0.15)
                

                if event.button == 8 and event.joy == 0:
                    print("button 8 is pressed on controller 0")
                    self.msg = "button 8 is pressed on controller 0"
                    self.server.send(self.msg.encode(self.FORMAT))
                    time.sleep(0.15)
                    

                if event.button == 9 and event.joy == 0:
                    print("button 9 is pressed on controller 0")
                    self.msg = "button 9 is pressed on controller 0"
                    self.server.send(self.msg.encode(self.FORMAT))
                    time.sleep(0.15)

                if event.button == 10 and event.joy == 0:
                    print("button 10 is pressed on controller 0")
                    self.msg = "button 10 is pressed on controller 0"
                    self.server.send(self.msg.encode(self.FORMAT))
                    time.sleep(0.15)

                if event.button == 11 and event.joy == 0:
                    print("button 11 is pressed on controller 0")
                    self.msg = "button 11 is pressed on controller 0"
                    self.server.send(self.msg.encode(self.FORMAT))
                    time.sleep(0.15)
                    

                # if event.button == 0 and event.joy == 1:
                #     print("button 0 is pressed on controller 1")
                #     msg = "button 0 is pressed on controller 1"
                #     server.send(msg.encode(FORMAT))
                #     time.sleep(0.15)

                # if event.button == 1 and event.joy == 1:
                #     print("button 1 is pressed on controller 1")
                #     msg = "button 1 is pressed on controller 1"
                #     server.send(msg.encode(FORMAT))
                #     time.sleep(0.15)

                # if event.button == 2 and event.joy == 1:
                #     print("button 2 is pressed on controller 1")
                #     msg = "button 2 is pressed on controller 1"
                #     server.send(msg.encode(FORMAT))
                #     time.sleep(0.15)

                # if event.button == 3 and event.joy == 1:
                #     print("button 3 is pressed on controller 1")
                #     msg = "button 3 is pressed on controller 1"
                #     server.send(msg.encode(FORMAT))
                #     time.sleep(0.15)

                # if event.button == 4 and event.joy == 1:
                #     print("button 4 is pressed on controller 1")
                #     msg = "button 4 is pressed on controller 1"
                #     server.send(msg.encode(FORMAT))
                #     time.sleep(0.15)

                # if event.button == 5 and event.joy == 1:
                #     print("button 5 is pressed on controller 1")
                #     msg = "button 5 is pressed on controller 1"
                #     server.send(msg.encode(FORMAT))
                #     time.sleep(0.15)

                # if event.button == 6 and event.joy == 1:
                #     print("button 6 is pressed on controller 1")
                #     msg = "button 6 is pressed on controller 1"
                #     server.send(msg.encode(FORMAT))
                #     time.sleep(0.15)

                # if event.button == 7 and event.joy == 1:
                #     print("button 7 is pressed on controller 1")
                #     msg = "button 7 is pressed on controller 1"
                #     server.send(msg.encode(FORMAT))
                #     time.sleep(0.15)

                # if event.button == 8 and event.joy == 1:
                #     print("button 8 is pressed on controller 1")
                #     msg = "button 8 is pressed on controller 1"
                #     server.send(msg.encode(FORMAT))
                #     time.sleep(0.15)

                # if event.button == 9 and event.joy == 1:
                #     print("button 9 is pressed on controller 1")
                #     msg = "button 9 is pressed on controller 1"
                #     server.send(msg.encode(FORMAT))
                #     time.sleep(0.15)

                # if event.button == 10 and event.joy == 1:
                #     print("button 10 is pressed on controller 1")
                #     msg = "button 10 is pressed on controller 1"
                #     server.send(msg.encode(FORMAT))
                #     time.sleep(0.15)

                # if event.button == 11 and event.joy == 1:
                #     print("button 11 is pressed on controller 1")
                #     msg = "button 11 is pressed on controller 1"
                #     server.send(msg.encode(FORMAT))
                #     time.sleep(0.15)

    ###################################################################################################

            if event.type == JOYHATMOTION:

                if event.value == (1,0) and event.joy == 0:             #slide right
                    print("right button is pressed on controller 0")
                    #self.msg = "move right"
                    self.server.send("move right".encode(self.FORMAT))
                    self.label_19.setText("Sliding right")
                    self.sr = True
                    time.sleep(0.15)

                elif event.value == (-1,0) and event.joy == 0:            #slide left
                    print("left button is pressed on controller 0")
                    #self.msg = "move left"
                    self.server.send("move left".encode(self.FORMAT))
                    self.label_19.setText("Sliding left")
                    self.sl = True
                    time.sleep(0.15)

                elif event.value == (0,-1) and event.joy == 0:            #move down
                    print("down button is pressed on controller 0")
                    #self.msg = "move down"
                    self.server.send("move down".encode(self.FORMAT))
                    self.label_19.setText("Descending")
                    self.md = True
                    time.sleep(0.15)

                elif event.value == (0,1) and event.joy == 0:             #move up
                    #print("up button is pressed on controller 0")
                    #self.msg = "move up"
                    self.server.send("move up".encode(self.FORMAT))
                    self.label_19.setText("Ascending")
                    self.mu = True
                    time.sleep(0.15)

                elif event.value == (0,0) and event.joy == 0:           #stops motion when you remove your hard from button
                    #self.msg = "move stop"
                    self.server.send("move stop".encode(self.FORMAT))
                    self.label_19.setText("Static")
                    time.sleep(0.25)

                    if self.sr == True:
                        self.server.send("done slideright".encode(self.FORMAT))
                        self.sr = False
                        time.sleep(0.15)
                    if self.sl == True:
                        self.server.send("done slideleft".encode(self.FORMAT))
                        self.sl = False
                        time.sleep(0.15)
                    if self.mu == True:
                        self.server.send("done moveup".encode(self.FORMAT))
                        self.mu = False
                        time.sleep(0.15)
                    if self.md == True:
                        self.server.send("done movedown".encode(self.FORMAT))
                        self.md = False
                        time.sleep(0.15)

                    


                # if event.value == (1,0) and event.joy == 1:
                #     print("right button is pressed on controller 1")
                #     msg = "right button is pressed on controller 1"
                #     server.send(msg.encode(FORMAT))
                #     time.sleep(0.15)

                # if event.value == (-1,0) and event.joy == 1:
                #     print("left button is pressed on controller 1")
                #     msg = "left button is pressed on controller 1"
                #     server.send(msg.encode(FORMAT))
                #     time.sleep(0.15)

                # if event.value == (0,-1) and event.joy == 1:
                #     print("down button is pressed on controller 1")
                #     msg = "down button is pressed on controller 1"
                #     server.send(msg.encode(FORMAT))
                #     time.sleep(0.15)

                # if event.value == (0,1) and event.joy == 1:
                #     print("up button is pressed on controller 1")
                #     msg = "up button is pressed on controller 1"
                #     server.send(msg.encode(FORMAT))
                #     time.sleep(0.15)

    ###################################################################################################

            if event.type == JOYAXISMOTION:          
                if pygame.joystick.Joystick(0).get_axis(0) >= 0.75 :        #rotate right
                    #print("move right from analog 0, controller 0")
                    #self.msg = "move yawcw"
                    self.server.send("move yawcw".encode(self.FORMAT))
                    self.label_19.setText("Rotating right")
                    self.rotr = True
                    time.sleep(0.15)
                
                elif pygame.joystick.Joystick(0).get_axis(0) <= -0.75 :       #rotate left
                    #print("move left from analog 0, controller 0")
                    #self.msg = "move yawccw"
                    self.server.send("move yawccw".encode(self.FORMAT))
                    self.label_19.setText("Rotating left")
                    self.rotr = True
                    time.sleep(0.15)

                elif pygame.joystick.Joystick(0).get_axis(1) >= 0.75 :        #move backward
                    #print("move backward from analog 0, controller 0")
                    #self.msg = "move backward"
                    # if self.rotr == True:
                    #     self.server.send("done pitchup".encode(self.FORMAT))
                    #     self.rotr = False
                    #     time.sleep(0.15)
                    # if self.rotl == True:
                    #     self.server.send("done pitchup".encode(self.FORMAT))
                    #     self.rotl = False
                    #     time.sleep(0.15)
                    self.server.send("move backward".encode(self.FORMAT))
                    self.label_19.setText("Moving backward")
                    time.sleep(0.15)


                elif pygame.joystick.Joystick(0).get_axis(1) <= -0.75 :       #move forward
                    #print("move forward from analog 0, controller 0")
                    #self.msg = "move forward"
                    # if self.rotr == True:
                    #     self.server.send("done pitchup".encode(self.FORMAT))
                    #     self.rotr = False
                    #     time.sleep(0.15)
                    # if self.rotl == True:
                    #     self.server.send("done pitchup".encode(self.FORMAT))
                    #     self.rotl = False
                    #     time.sleep(0.15)
                    self.server.send("move forward".encode(self.FORMAT))
                    self.label_19.setText("Moving forward")
                    time.sleep(0.15)


                # if pygame.joystick.Joystick(1).get_axis(0) >= 0.75 :        
                #     print("move right from analog 0, controller 1")
                #     msg = "move right from analog 0, controller 1"
                #     server.send(msg.encode(FORMAT))
                #     time.sleep(0.15)
                
                # if pygame.joystick.Joystick(1).get_axis(0) <= -0.75 :
                #     print("move left from analog 0, controller 1")
                #     msg = "move left from analog 0, controller 1"
                #     server.send(msg.encode(FORMAT))
                #     time.sleep(0.15)

                # if pygame.joystick.Joystick(1).get_axis(1) >= 0.75 :
                #     print("move down from analog 0, controller 1")
                #     msg = "move down from analog 0, controller 1"
                #     server.send(msg.encode(FORMAT))
                #     time.sleep(0.15)

                # if pygame.joystick.Joystick(1).get_axis(1) <= -0.75 :
                #     print("move up from analog 0, controller 1")
                #     msg = "move up from analog 0, controller 1"
                #     server.send(msg.encode(FORMAT))
                #     time.sleep(0.15)

                
                if pygame.joystick.Joystick(0).get_axis(3) >= 0.75 :        #roll right
                    #print("move right from analog 1, controller 0")
                    #self.msg = "move rolltoright"
                    # if self.pd == True:
                    #     self.server.send("done pitchdown".encode(self.FORMAT))
                    #     self.pd = False
                    #     time.sleep(0.15)
                    # if self.pu == True:
                    #     self.server.send("done pitchup".encode(self.FORMAT))
                    #     self.pu = False
                    #     time.sleep(0.15)
                    self.server.send("move rolltoright".encode(self.FORMAT))
                    self.label_19.setText("Rolling right")
                    self.rolr = True
                    time.sleep(0.15)
                


                elif pygame.joystick.Joystick(0).get_axis(3) <= -0.75 :       #roll left
                    #print("move left from analog 1, controller 0")
                    #self.msg = "move rolltoleft"
                    # if self.pd == True:
                    #     self.server.send("done pitchdown".encode(self.FORMAT))
                    #     self.pd = False
                    #     time.sleep(0.15)
                    # if self.pu == True:
                    #     self.server.send("done pitchup".encode(self.FORMAT))
                    #     self.pu = False
                    #     time.sleep(0.15)
                    self.server.send("move rolltoleft".encode(self.FORMAT))
                    self.label_19.setText("Rolling left")
                    self.roll = True
                    time.sleep(0.15)



                elif pygame.joystick.Joystick(0).get_axis(2) >= 0.75 :        #pitch up
                    #print("move down from analog 1, controller 0")
                    #self.msg = "move pitchup"
                    # if self.rolr == True:
                    #     self.server.send("done rollright".encode(self.FORMAT))
                    #     self.rolr = False
                    #     time.sleep(0.15)
                    # if self.roll == True:
                    #     self.server.send("done rollleft".encode(self.FORMAT))
                    #     self.roll = False
                    #     time.sleep(0.15)

                    self.server.send("move pitchup".encode(self.FORMAT))
                    self.label_19.setText("Pitching up")
                    self.pu = True
                    time.sleep(0.15)



                elif pygame.joystick.Joystick(0).get_axis(2) <= -0.75 :       #pitch down
                    #print("move up from analog 1, controller 0")
                    #self.msg = "move pitchdown"
                    # if self.rolr == True:
                    #     self.server.send("done rollright".encode(self.FORMAT))
                    #     self.rolr = False
                    #     time.sleep(0.15)
                    # if self.roll == True:
                    #     self.server.send("done rollleft".encode(self.FORMAT))
                    #     self.roll = False
                    #     time.sleep(0.15)
                    self.server.send("move pitchdown".encode(self.FORMAT))
                    self.label_19.setText("Pitching down")
                    self.pd = True
                    time.sleep(0.15)



                elif ((pygame.joystick.Joystick(0).get_axis(0) >= -0.1) and (pygame.joystick.Joystick(0).get_axis(0) <= 0.1) and 
                    (pygame.joystick.Joystick(0).get_axis(1) >= -0.1) and (pygame.joystick.Joystick(0).get_axis(1) <= 0.1)  and
                    (pygame.joystick.Joystick(0).get_axis(3) >= -0.1) and (pygame.joystick.Joystick(0).get_axis(3) <= 0.1)  and 
                    (pygame.joystick.Joystick(0).get_axis(2) >= -0.1) and (pygame.joystick.Joystick(0).get_axis(2) <= 0.1))  :     #stops motion if both analogs are not at motion positions
                    #self.msg = "move stop"
                    print("move stop" + " : from analog 0 controller 0")
                    self.server.send("move stop".encode(self.FORMAT))
                    self.label_19.setText("Static")
                    time.sleep(0.25)

                    

                # if pygame.joystick.Joystick(1).get_axis(3) >= 0.75 :
                #     print("move right from analog 1, controller 1")
                #     msg = "move right from analog 1, controller 1"
                #     server.send(msg.encode(FORMAT))
                #     time.sleep(0.15)
                
                # if pygame.joystick.Joystick(1).get_axis(3) <= -0.75 :
                #     print("move left from analog 1, controller 1")
                #     msg = "move left from analog 1, controller 1"
                #     server.send(msg.encode(FORMAT))
                #     time.sleep(0.15)

                # if pygame.joystick.Joystick(1).get_axis(2) >= 0.75 :
                #     print("move down from analog 1, controller 1")
                #     msg = "move down from analog 1, controller 1"
                #     server.send(msg.encode(FORMAT))
                #     time.sleep(0.15)

                # if pygame.joystick.Joystick(1).get_axis(2) <= -0.75 :
                #     print("move up from analog 1, controller 1")
                #     msg = "move up from analog 1, controller 1"
                #     server.send(msg.encode(FORMAT))
                #     time.sleep(0.15)



###################################################################################################
###################################################################################################

    def receive(self):
        '''
        #while True:
        while self.connected:
            print(self.connected)
        #if self.connected:
        
            self.msg = self.server.recv(128).decode()
            print(self.msg)
            time.sleep(0.15)'''

        while True:
            if self.connected:
                
                # sockets_list = [sys.stdin, self.server]
                # read_sockets,write_socket, error_socket = select.select(sockets_list,[],[])
                # for socks in read_sockets:
                #     if socks == self.server:
                #         self.msg = (socks.recv(2048)).decode('utf-8')
                #         print(self.msg)
                #         if "pitch" in self.msg:
                #             pitch = self.msg.split()
                #             self.label_9.setText(pitch[1])

                self.msg = (self.server.recv(2048)).decode('utf-8')
                print(self.msg)

                if "pitch" in self.msg:
                    pitch = self.msg.split()
                    self.label_9.setText(pitch[1])

                if "roll" in self.msg:
                    roll = self.msg.split()
                    self.label_8.setText(roll[1])
            
                if "rotate" in self.msg:
                    rotate = self.msg.split()
                    self.label_5.setText(rotate[1])

                if "temp" in self.msg:
                    temp = self.msg.split()
                    self.label_7.setText(temp[1])

                if "hight" in self.msg:
                    hight = self.msg.split()
                    self.label_6.setText(hight[1])


###################################################################################################
###################################################################################################

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainApp("")  #object
    window.show()       #shows the window
    #app.exec_()         #infinite loop
    
    while True:
        try:
            window.send_msg()
        except:
            pass

        # try:
        #     window.receive()
        # except:
        #     pass


    sys.exit(app.exec_())
    
