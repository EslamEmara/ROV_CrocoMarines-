import socket
import select
import sys
import threading


#IP = "127.0.0.1"
IP = socket.gethostbyname(socket.gethostname())
PORT = 8000
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind((IP, PORT))

server.listen(100)
print("[LISTENING] server is listening...")
print("[IP]", IP)

clients = []

def client_handle(conn, addr):
	while True:
			try:
				message = (conn.recv(2048)).decode('utf-8')
				if message:
					print ("<" + addr[0] + "> " + message)
					send_to_clients(message, conn)
				else:
					if conn in clients:
						clients.remove(conn)
			except:
				continue
def send_to_clients(message, connection):
	for client in clients:
		if client!=connection:
			try:
				client.send(message.encode('utf-8'))
			except:
				client.close()
				if client in clients:
					clients.remove(client)
while True:
	try:
		conn, addr = server.accept()
		clients.append(conn)
	except:
		pass
	print (addr[0] + " connected")

	x= threading.Thread(target=client_handle,args=(conn,addr))
	x.start()


conn.close()
server.close()
