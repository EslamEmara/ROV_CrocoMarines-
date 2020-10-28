import socket
import threading
PORT = 8000
FORMAT = 'utf-8'
IP = "127.0.0.1"
#IP = socket.gethostbyname(socket.gethostname())                 #sets ip as the ip of the device 
ADDR = (IP,PORT)
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    server.connect(ADDR)
    print(f"[CONNECTION] successfully connected to {ADDR} \n")
except:
    pass

pid_msg = ''
def set_msg_variable(msg):
    global pid_msg
    pid_msg = msg

class IMUClass():
    def __init__(self):
        msg = ''
        self.msg = msg
        #self.msg1 = msg1
        
        thread1 = threading.Thread(target = self.receive )
        thread2 = threading.Thread(target = self.send_msg, args=(msg,) )
        thread1.start()
        thread2.start()

    def receive(self):
        while True:
            self.msg = server.recv(128).decode()
            if self.msg:
                set_msg_variable(self.msg)

    def send_msg(self, msg1):
        if msg1:
            server.send(msg1.encode(FORMAT))
            # print("sendt",msg1)

#how to use:

# obj = IMUClass()
# obj.send_msg("take this as msg1")
# obj.send_msg("pitch 50")
