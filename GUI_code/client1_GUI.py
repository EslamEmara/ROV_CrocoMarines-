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
from PyQt5 import QtCore, QtGui
from PyQt5.QtCore import QCoreApplication

FORM_CLASS, _ = loadUiType(path.join(path.dirname(__file__), "client1.ui"))

class MainApp(QMainWindow , FORM_CLASS):
    def __init__(self, msg, parent=None):
        super(MainApp , self).__init__(parent)
        QMainWindow.__init__(self)

        self.FORMAT = 'utf-8'
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        pygame.init()
        self.joystick_count = pygame.joystick.get_count()
        print("Number of joysticks:",format(self.joystick_count) )

        for i in range(self.joystick_count):
            self.joystick = pygame.joystick.Joystick(i)
            self.joystick.init()
            print("initialized joystick",i)

        self.speed = 0
        self.msg = msg
        self.connected = False
        self.micro_active = False
        self.controller0 = 0
        self.controller1 = 1
        self.time_started = False
        
        thread_02 = threading.Thread(target = self.receive, args=())
        thread_02.start()

        self.setupUi(self)
        self.Handel_UI()
        self.Handel_Buttons()

    def closeEvent(self, event):
        reply = QMessageBox.question(self, 'Close Confirmation', 'Are you sure you want to close?',
            	QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            event.accept()
            if self.connected:
                self.server.send("[DISCONNECT] Client Disconnected.".encode(self.FORMAT))
                self.server.shutdown(socket.SHUT_RDWR)
                self.server.close()
        else:
            event.ignore()

    def Handel_UI(self):
        self.setWindowTitle('Croco GUI')
        self.setFixedSize(751, 655)
        self.lineEdit_2.setMaxLength(5)
        self.lineEdit.setMaxLength(13)
        self.lineEdit_2.setValidator(QIntValidator())   #only allows int type of input

    def Handel_Buttons(self):
        self.pushButton.clicked.connect(self.start)
        self.pushButton_2.clicked.connect(self.Disconnect)

    def Disconnect(self):
        if self.connected:
            self.close()
            time.sleep(1)
        else:
            pass
        
    def start(self):
        try:
            PORT = int(self.lineEdit_2.text())
            IP = self.lineEdit.text()
            self.server.connect((IP, PORT))
            print(f"[CONNECTION] successfully connected to {(IP, PORT)} \n")
            self.connected = True
        except:
            pass

        if self.connected == True:
            self.label_14.setText("Connected")
            self.lineEdit_2.setReadOnly(True)
            self.lineEdit.setReadOnly(True)

    def count_up(self):
        seconds = 900
        self.time_started = True
        for j in range(1,seconds+1):
            mins = j/60
            j = j%60
            mins = int(mins%60)
            self.label_50.setText(f"{mins}:{j}")
            time.sleep(1)
        self.label_50.setText("Time's up!")
            
###################################################################################################

    def send_msg(self):
        for event in pygame.event.get():    #loops on events of pygame library

            if event.type == JOYBUTTONDOWN:     #if event is button down on controller
                if event.button == 0 and event.joy == self.controller0:            #move servo gripper to neutral position when triangle is pressed on controller 0
                    self.server.send("sgrip n".encode(self.FORMAT))
                    time.sleep(0.15)

                if event.button == 1 and event.joy == self.controller0:            #move servo gripper to right position 90 degree from neutral when circle is pressed on controller 0
                    self.server.send("sgrip r".encode(self.FORMAT))
                    time.sleep(0.15)

                if event.button == 3 and event.joy == self.controller0:            #move servo gripper to left position 90 degree from neutral when square is pressed on controller 0
                    self.server.send("sgrip l".encode(self.FORMAT))
                    time.sleep(0.15)

                if event.button == 4 and event.joy == self.controller0:         #camera up with L1 when pressed on controller 0
                    self.server.send("cam up".encode(self.FORMAT))
                    time.sleep(0.15)

                if event.button == 5 and event.joy == self.controller0:        #speed up with R1 when pressed on controller 0
                    self.speed = self.speed +30
                    if self.speed >= 150 :
                        self.speed = 150
                    self.msg = "speed " + str(self.speed)
                    self.server.send(self.msg.encode(self.FORMAT))
                    self.label_4.setText(str(self.speed+90))
                    time.sleep(0.15)

                if event.button == 6 and event.joy == self.controller0:           #camera down with L2 when pressed on controller 0
                    self.server.send("cam down".encode(self.FORMAT)) 
                    time.sleep(0.15)       
                    
                if event.button == 7 and event.joy == self.controller0:         #speed down with R2 when pressed  on controller 0        
                    self.speed = self.speed - 30
                    if self.speed <= 0 :
                        self.speed = 0
                    self.msg = "speed " + str(self.speed)
                    self.server.send(self.msg.encode(self.FORMAT))
                    self.label_4.setText(str(self.speed+90))
                    time.sleep(0.15)

                if event.button == 8 and event.joy == self.controller0:        #connects when start button on controller 0 is pressed 
                    if self.connected == True and self.time_started == False:
                        self.time_started = True
                        thread_01 = threading.Thread(target = self.count_up, args=())
                        thread_01.start()
                    
                if event.button == 9 and event.joy == self.controller0:        #connects when start button on controller 0 is pressed 
                    self.start()

                if event.button == 10 and event.joy == self.controller0:            #closes the servo dc gripper of ROV when right analog button is pressed on controller 0
                    self.server.send("grip close".encode(self.FORMAT))
                    self.label_27.setText("Closed")
                    time.sleep(0.15)
                
                if event.button == 11 and event.joy == self.controller0:        #opens the servo dc gripper of ROV when right analog button is pressed on controller 0
                    self.server.send("grip open".encode(self.FORMAT))
                    self.label_27.setText("Opened")
                    time.sleep(0.15)

                if event.button == 9 and event.joy == self.controller1 and self.connected == True:     #Activates micro ROV when start is pressed on controller 1
                    self.micro_active = True
                    if self.connected:
                        self.label_24.setText("Connected")

                if event.button == 8 and event.joy == self.controller1 and self.connected == True:    #Deactivates micro ROV when select is pressed on controller 1
                    self.micro_active = False
                    self.label_24.setText("Disconnected")

                if event.button == 10 and event.joy == self.controller1 and (self.micro_active == True):    #closes the dc gripper of micoro ROV when left analog button is pressed on controller 1
                    self.server.send("micro close".encode(self.FORMAT))
                    self.label_29.setText("Closed")
                    time.sleep(0.15)

                if event.button == 11 and event.joy == self.controller1 and (self.micro_active == True):    #opens the dc gripper of micoro ROV when right analog button is pressed on controller 1
                    self.server.send("micro open".encode(self.FORMAT))
                    self.label_29.setText("Opened")
                    time.sleep(0.15)

#############################################################################################################

            if event.type == JOYBUTTONUP:
                if event.button == 4 and event.joy == self.controller0:         #camera stops when L1 is released
                    self.server.send("cam stop".encode(self.FORMAT))
                    time.sleep(0.15)

                if event.button == 6 and event.joy == self.controller0:           #camera stops when L2 is released
                    self.server.send("cam stop".encode(self.FORMAT)) 
                    time.sleep(0.15) 
                    
#############################################################################################################

            if event.type == JOYHATMOTION:
                if event.value == (1,0) and event.joy == self.controller0:             #slide right
                    self.server.send("move right".encode(self.FORMAT))
                    self.label_19.setText("Sliding right")
                    time.sleep(0.15)

                elif event.value == (-1,0) and event.joy == self.controller0:            #slide left
                    self.server.send("move left".encode(self.FORMAT))
                    self.label_19.setText("Sliding left")
                    time.sleep(0.15)

                elif event.value == (0,-1) and event.joy == self.controller0:            #move down
                    self.server.send("move down".encode(self.FORMAT))
                    self.label_19.setText("Descending")
                    time.sleep(0.15)

                elif event.value == (0,1) and event.joy == self.controller0:             #move up
                    self.server.send("move up".encode(self.FORMAT))
                    self.label_19.setText("Ascending")
                    time.sleep(0.15)

                elif event.value == (0,0) and event.joy == self.controller0:           #stops motion when you remove your hard from button
                    self.server.send("move stop".encode(self.FORMAT))
                    self.label_19.setText("Static")
                    time.sleep(0.15)

    ###################################################################################################

            if event.type == JOYAXISMOTION:          
                if pygame.joystick.Joystick(self.controller0).get_axis(0) >= 0.98 :        #rotate right
                    self.server.send("move yawcw".encode(self.FORMAT))
                    self.label_19.setText("Rotating right")
                    time.sleep(0.15)
                
                elif pygame.joystick.Joystick(self.controller0).get_axis(0) <= -1 :       #rotate left
                    self.server.send("move yawccw".encode(self.FORMAT))
                    self.label_19.setText("Rotating left")
                    time.sleep(0.15)

                elif pygame.joystick.Joystick(self.controller0).get_axis(1) >= 0.98 :        #move backward
                    self.server.send("move backward".encode(self.FORMAT))
                    self.label_19.setText("Moving backward")
                    time.sleep(0.15)

                elif pygame.joystick.Joystick(self.controller0).get_axis(1) <= -1 :       #move forward
                    self.server.send("move forward".encode(self.FORMAT))
                    self.label_19.setText("Moving forward")
                    time.sleep(0.15)
                
                elif pygame.joystick.Joystick(self.controller0).get_axis(3) >= 0.98 :        #roll right
                    self.server.send("move rolltoright".encode(self.FORMAT))
                    self.label_19.setText("Rolling right")
                    time.sleep(0.15)
                
                elif pygame.joystick.Joystick(self.controller0).get_axis(3) <= -1 :       #roll left
                    self.server.send("move rolltoleft".encode(self.FORMAT))
                    self.label_19.setText("Rolling left")
                    time.sleep(0.15)

                elif pygame.joystick.Joystick(self.controller0).get_axis(2) >= 0.98 :        #pitch up
                    self.server.send("move pitchup".encode(self.FORMAT))
                    self.label_19.setText("Pitching up")
                    time.sleep(0.15)

                elif pygame.joystick.Joystick(self.controller0).get_axis(2) <= -1 :       #pitch down
                    self.server.send("move pitchdown".encode(self.FORMAT))
                    self.label_19.setText("Pitching down")
                    time.sleep(0.15)

                elif ((pygame.joystick.Joystick(self.controller1).get_axis(0) >= -0.1) and (pygame.joystick.Joystick(self.controller1).get_axis(0) <= 0.1) and
                    (pygame.joystick.Joystick(self.controller1).get_axis(1) >= -0.1) and (pygame.joystick.Joystick(self.controller1).get_axis(1) <= 0.1)   and
                    (pygame.joystick.Joystick(self.controller1).get_axis(3) >= -0.1) and (pygame.joystick.Joystick(self.controller1).get_axis(3) <= 0.1)   and 
                    (pygame.joystick.Joystick(self.controller1).get_axis(2) >= -0.1) and (pygame.joystick.Joystick(self.controller1).get_axis(2) <= 0.1)   and
                    (pygame.joystick.Joystick(self.controller0).get_axis(0) >= -0.1) and (pygame.joystick.Joystick(self.controller0).get_axis(0) <= 0.1)   and 
                    (pygame.joystick.Joystick(self.controller0).get_axis(1) >= -0.1) and (pygame.joystick.Joystick(self.controller0).get_axis(1) <= 0.1)   and
                    (pygame.joystick.Joystick(self.controller0).get_axis(3) >= -0.1) and (pygame.joystick.Joystick(self.controller0).get_axis(3) <= 0.1)   and 
                    (pygame.joystick.Joystick(self.controller0).get_axis(2) >= -0.1) and (pygame.joystick.Joystick(self.controller0).get_axis(2) <= 0.1)) :     
                    self.server.send("move stop".encode(self.FORMAT))     #stops ROV motion if both analogs are not at motion positions
                    self.label_19.setText("Static")
                    time.sleep(0.15)

###################################################################################################

            if (event.type == JOYAXISMOTION) and (self.micro_active == True):
                if pygame.joystick.Joystick(self.controller1).get_axis(1) >= 0.98 :        #move micro ROV backward
                    self.server.send("micro backward".encode(self.FORMAT))
                    self.label_21.setText("Backward")
                    time.sleep(0.15)

                elif pygame.joystick.Joystick(self.controller1).get_axis(1) <= -0.99 :       #move micro ROV forward
                    self.server.send("micro forward".encode(self.FORMAT))
                    self.label_21.setText("Forward")
                    time.sleep(0.15)

                elif ((pygame.joystick.Joystick(self.controller1).get_axis(0) >= -0.1) and (pygame.joystick.Joystick(self.controller1).get_axis(0) <= 0.1) and
                    (pygame.joystick.Joystick(self.controller1).get_axis(1) >= -0.1) and (pygame.joystick.Joystick(self.controller1).get_axis(1) <= 0.1)   and
                    (pygame.joystick.Joystick(self.controller1).get_axis(3) >= -0.1) and (pygame.joystick.Joystick(self.controller1).get_axis(3) <= 0.1)   and 
                    (pygame.joystick.Joystick(self.controller1).get_axis(2) >= -0.1) and (pygame.joystick.Joystick(self.controller1).get_axis(2) <= 0.1)   and
                    (pygame.joystick.Joystick(self.controller0).get_axis(0) >= -0.1) and (pygame.joystick.Joystick(self.controller0).get_axis(0) <= 0.1)   and 
                    (pygame.joystick.Joystick(self.controller0).get_axis(1) >= -0.1) and (pygame.joystick.Joystick(self.controller0).get_axis(1) <= 0.1)   and
                    (pygame.joystick.Joystick(self.controller0).get_axis(3) >= -0.1) and (pygame.joystick.Joystick(self.controller0).get_axis(3) <= 0.1)   and 
                    (pygame.joystick.Joystick(self.controller0).get_axis(2) >= -0.1) and (pygame.joystick.Joystick(self.controller0).get_axis(2) <= 0.1)) :
                    self.server.send("micro stop".encode(self.FORMAT))   #stops micro ROV motion if both analogs are not at motion positions
                    self.label_21.setText("Static")
                    time.sleep(0.15)

###################################################################################################

    def receive(self):
        while True:
            if self.connected:
                self.msg = (self.server.recv(2048)).decode('utf-8')
                print(self.msg)

                if "angel" in self.msg:
                    angel = self.msg.split()
                    self.label_9.setText(angel[1])
                    self.label_8.setText(angel[2])
                    self.label_5.setText(angel[3])
                    self.label_7.setText(angel[4])
                    self.label_6.setText(angel[5])

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
    sys.exit(app.exec_())

###################################################################################################