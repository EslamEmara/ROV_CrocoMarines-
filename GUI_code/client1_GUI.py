import time
import socket
import threading
import pygame
from pygame.locals import*
import sys
import os
from os import path

import PyQt5
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUiType
from PyQt5 import QtCore
from PyQt5.QtCore import QCoreApplication

FORM_CLASS, _ = loadUiType(path.join(path.dirname(__file__), "client1.ui"))

class MainApp(QMainWindow , FORM_CLASS):
    def __init__(self, msg, parent=None):
        super(MainApp , self).__init__(parent)
        QMainWindow.__init__(self)

        self.FORMAT = 'utf-8'
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        pygame.init()
        self.screen = pygame.display.set_mode((1,1))
        #pygame.display.set_caption("Joystick Testing")
        #pygame.display.iconify()

        self.joystick_count = pygame.joystick.get_count()
        print("Number of joysticks:",format(self.joystick_count) )

        for i in range(self.joystick_count):
            self.joystick = pygame.joystick.Joystick(i)
            self.joystick.init()
            print("initialized joystick",i)

        self.speed = 0
        # self.RUN = True
        self.msg = msg
        self.connected = False
        
        thread_02 = threading.Thread(target = self.receive, args=())
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
            self.label_4.setText("90")
            self.lineEdit_2.setReadOnly(True)
            self.lineEdit.setReadOnly(True)
            
###################################################################################################

    def send_msg(self):
        for event in pygame.event.get():

            # if event.type == pygame.QUIT:
            #     print ("Received event 'Quit', exiting.")
            #     break

            if event.type == KEYDOWN and event.key == K_KP_ENTER :
                self.start()

            if event.type == JOYBUTTONDOWN:

                # if event.button == 0 and event.joy == 0:        
                #     print("button 0 is pressed on controller 0")
                #     self.msg = "button 0 is pressed on controller 0"
                #     self.server.send(self.msg.encode(self.FORMAT))
                #     time.sleep(0.15)

                # if event.button == 1 and event.joy == 0:
                #     print("button 1 is pressed on controller 0")
                #     self.msg = "button 1 is pressed on controller 0"
                #     self.server.send(self.msg.encode(self.FORMAT))
                #     time.sleep(0.15)

                #if event.button == 2 and event.joy == 0:        #connects when pressing x button on controller 0    
                    #self.start()

                # if event.button == 3 and event.joy == 0:
                #     print("button 3 is pressed on controller 0")
                #     self.msg = "button 3 is pressed on controller 0"
                #     self.server.send(self.msg.encode(self.FORMAT))
                #     time.sleep(0.15)

                # if event.button == 4 and event.joy == 0:
                #     print("button 4 is pressed on controller 0")
                #     self.msg = "button 4 is pressed on controller 0"
                #     self.server.send(self.msg.encode(self.FORMAT))
                #     time.sleep(0.15)

                # if event.button == 5 and event.joy == 0:
                #     print("button 5 is pressed on controller 0")
                #     self.msg = "button 5 is pressed on controller 0"
                #     self.server.send(self.msg.encode(self.FORMAT))
                #     time.sleep(0.15)

                if event.button == 6 and event.joy == 0:            #speed down
                    self.speed = self.speed - 30
                    if self.speed <= 0 :
                        self.speed = 0
                    self.msg = "speed " + str(self.speed)
                    self.server.send(self.msg.encode(self.FORMAT))
                    self.label_4.setText(str(self.speed+90))
                    time.sleep(0.15)
                    
                if event.button == 7 and event.joy == 0:            #speed up                
                    self.speed = self.speed +30
                    if self.speed >= 150 :
                        self.speed = 150
                    self.msg = "speed " + str(self.speed)
                    self.server.send(self.msg.encode(self.FORMAT))
                    self.label_4.setText(str(self.speed+90))
                    time.sleep(0.15)
                
                # if event.button == 8 and event.joy == 0:
                #     print("button 8 is pressed on controller 0")
                #     self.msg = "button 8 is pressed on controller 0"
                #     self.server.send(self.msg.encode(self.FORMAT))
                #     time.sleep(0.15)
                    
                if event.button == 9 and event.joy == 0:        #connects when pressing start button on controller 0   
                    self.start()

                # if event.button == 10 and event.joy == 0:
                #     print("button 10 is pressed on controller 0")
                #     self.msg = "button 10 is pressed on controller 0"
                #     self.server.send(self.msg.encode(self.FORMAT))
                #     time.sleep(0.15)

                # if event.button == 11 and event.joy == 0:
                #     print("button 11 is pressed on controller 0")
                #     self.msg = "button 11 is pressed on controller 0"
                #     self.server.send(self.msg.encode(self.FORMAT))
                #     time.sleep(0.15)
                    
#############################################################################################################

            if event.type == JOYHATMOTION:
                if event.value == (1,0) and event.joy == 0:             #slide right
                    self.server.send("move right".encode(self.FORMAT))
                    self.label_19.setText("Sliding right")
                    time.sleep(0.15)

                elif event.value == (-1,0) and event.joy == 0:            #slide left
                    self.server.send("move left".encode(self.FORMAT))
                    self.label_19.setText("Sliding left")
                    time.sleep(0.15)

                elif event.value == (0,-1) and event.joy == 0:            #move down
                    self.server.send("move down".encode(self.FORMAT))
                    self.label_19.setText("Descending")
                    time.sleep(0.15)

                elif event.value == (0,1) and event.joy == 0:             #move up
                    self.server.send("move up".encode(self.FORMAT))
                    self.label_19.setText("Ascending")
                    time.sleep(0.15)

                elif event.value == (0,0) and event.joy == 0:           #stops motion when you remove your hard from button
                    self.server.send("move stop".encode(self.FORMAT))
                    self.label_19.setText("Static")
                    time.sleep(0.15)

    ###################################################################################################

            if event.type == JOYAXISMOTION:          
                if pygame.joystick.Joystick(0).get_axis(0) >= 0.95 :        #rotate right
                    #self.msg = "move yawcw"
                    self.server.send("move yawcw".encode(self.FORMAT))
                    self.label_19.setText("Rotating right")
                    time.sleep(0.15)
                
                elif pygame.joystick.Joystick(0).get_axis(0) <= -0.95 :       #rotate left
                    #self.msg = "move yawccw"
                    self.server.send("move yawccw".encode(self.FORMAT))
                    self.label_19.setText("Rotating left")
                    time.sleep(0.15)

                elif pygame.joystick.Joystick(0).get_axis(1) >= 0.95 :        #move backward
                    #self.msg = "move backward"
                    self.server.send("move backward".encode(self.FORMAT))
                    self.label_19.setText("Moving backward")
                    time.sleep(0.15)

                elif pygame.joystick.Joystick(0).get_axis(1) <= -0.95 :       #move forward
                    #self.msg = "move forward"
                    self.server.send("move forward".encode(self.FORMAT))
                    self.label_19.setText("Moving forward")
                    time.sleep(0.15)

                
                if pygame.joystick.Joystick(0).get_axis(3) >= 0.9 :        #roll right
                    #self.msg = "move rolltoright"
                    self.server.send("move rolltoright".encode(self.FORMAT))
                    self.label_19.setText("Rolling right")
                    time.sleep(0.15)
                
                elif pygame.joystick.Joystick(0).get_axis(3) <= -0.9 :       #roll left
                    #self.msg = "move rolltoleft"
                    self.server.send("move rolltoleft".encode(self.FORMAT))
                    self.label_19.setText("Rolling left")
                    time.sleep(0.15)

                elif pygame.joystick.Joystick(0).get_axis(2) >= 0.9 :        #pitch up
                    #self.msg = "move pitchup"
                    self.server.send("move pitchup".encode(self.FORMAT))
                    self.label_19.setText("Pitching up")
                    time.sleep(0.15)

                elif pygame.joystick.Joystick(0).get_axis(2) <= -0.9 :       #pitch down
                    #self.msg = "move pitchdown"
                    self.server.send("move pitchdown".encode(self.FORMAT))
                    self.label_19.setText("Pitching down")
                    time.sleep(0.15)

                elif ((pygame.joystick.Joystick(0).get_axis(0) >= -0.2) and (pygame.joystick.Joystick(0).get_axis(0) <= 0.2) and 
                    (pygame.joystick.Joystick(0).get_axis(1) >= -0.2) and (pygame.joystick.Joystick(0).get_axis(1) <= 0.2)  and
                    (pygame.joystick.Joystick(0).get_axis(3) >= -0.2) and (pygame.joystick.Joystick(0).get_axis(3) <= 0.2)  and 
                    (pygame.joystick.Joystick(0).get_axis(2) >= -0.2) and (pygame.joystick.Joystick(0).get_axis(2) <= 0.2))  :     #stops motion if both analogs are not at motion positions
                    #self.msg = "move stop"
                    self.server.send("move stop".encode(self.FORMAT))
                    self.label_19.setText("Static")
                    time.sleep(0.15)

###################################################################################################
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
        while True:
            if self.connected:
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
    
    #while True:
    while True:
        try:
            window.send_msg()
        except:
            pass

    sys.exit(app.exec_())