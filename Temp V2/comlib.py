import socket
import threading


class Client:
    # Member variables, will be assigned and used below (with self.<VARIABLE_NAME>
    client_socket = 0					# client socket used to send and receive data
    is_connected = 0					# Flag
    on_receive_func = 0					# Function to call whenever new data received

    def __init__(self):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


    # Public Functions

    def on_receive(self, func):
        self.on_receive_func = func			# Save the passed function in this object

    def start(self, server_ip="", server_port=8000):
        try:
            self.client_socket.connect((server_ip, server_port))
            self.is_connected = True
            print("connected to ({}:{})".format(server_ip, server_port))
        
            threading.Thread(target=self.receiving).start()	# Start the receiving function in separate thread
        except:
            print("Couldn't connect to server")
        
    def send(self, data):
        self.client_socket.send(bytes(data, "utf-8"))


    # Private Functions

    def disconnect(self):
        self.is_connected = False
        self.client_socket.shutdown(socket.SHUT_RDWR)	# Shutdown with read and write (RD..WR) will interrupt the socket recv(1024) function

    def receiving(self):
        while (self.is_connected):
            data = self.client_socket.recv(1024)	# The program execution will stuck here till there is data to receive or the socket is shutdown
            if data == b'':
                break
            data = data.decode("utf-8")
            self.on_receive_func(data)			# Call the on_receive_func and pass the received data
