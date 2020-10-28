import socket
import select
import sys
import threading

#IP = "127.0.0.1"
IP = socket.gethostbyname(socket.gethostname())		#gets ip of device
PORT = 8000
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)	#solves problem when port is already taken
server.bind((IP, PORT))		#binding to ip and port

server.listen(100)		#listening for clients
print("[LISTENING] server is listening...")
print("[IP]", IP)	#showing current ip

clients = []	#list of clients joined

def client_handle(conn, addr):
	while True:
			try:
				message = (conn.recv(2048)).decode('utf-8')	#if there is a message to recieve
				if message:		#if its not empty
					print ("<" + addr[0] + "> " + message)	#print the addr of the sender and the message
					send_to_clients(message, conn)		#sends the message to clients on group
				else:
					if conn in clients:		#if there is an error in connection and the client connection is in list of clients remove him
						clients.remove(conn)
			except:
				continue

def send_to_clients(message, connection):
	for client in clients:		#loops on all clients in list of clients
		if client!=connection:		#if the client is not the one who sent
			try:		#try sending message to him
				client.send(message.encode('utf-8'))
			except:		#if there is error in connection then close his connection 
				client.close()
				if client in clients:	#and if he is in the list of clients remove him
					clients.remove(client)
					
while True:	#main loop
	try:		#trys accepting new client 
		conn, addr = server.accept()	#the loop stops here until a new client connects
		clients.append(conn)		#add him to list of clients
	except:
		pass
	print (addr[0] + " connected")		#print his address and he is conneced

	x= threading.Thread(target=client_handle,args=(conn,addr))	#defining thread on client_handle function
	x.start()	#starts thread