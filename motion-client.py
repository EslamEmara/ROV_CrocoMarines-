from ConnectionWithGUI import ControlMotion
import socket
import threading

class MotionClass():
    def __init__(self):
        PORT = 8000
        FORMAT = 'utf-8'
        DISCONNECT_MSG = "!DISCONNECT"
        IP = socket.gethostbyname(socket.gethostname())
        ADDR = (IP,PORT)
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        msg = ''
        self.msg = msg

        self.ObjectFromMotion=ControlMotion()  # take object from motion part

        try:
            self.server.connect(ADDR)
            print(f"[CONNECTION] successfully connected to {ADDR} \n")
        except:
            pass

        thread = threading.Thread(target = self.receive )
        thread.start()

    def receive(self):
        while True:
            self.msg = self.server.recv(128).decode()
            self.ObjectFromMotion.DirectionofTravel(self.msg)  # send msg to Motion Part
            #print(msg)