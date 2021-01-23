#!/usr/bin/python3
from time import sleep
from threading import Thread
import threading
import socket
global run
#global varaibles
run=True
s= socket.socket(socket.AF_INET, socket.SOCK_STREAM) #Define parameters for socket connection
class server():

    def __init__(self):
        self.chatting = False #Not Chatting
        self.old_client=0

    def start(self):
        HOST = 'localhost'
        PORT = 8019
        s.bind((HOST, PORT)) #bind port and host
        s.listen(5) # Number of connections
        print("Server started")

    def connections(self):
        numclient=0 # set the number of clients to zero
        while True:
            self.client, self.address = s.accept() # Accept connections
            print("Connected to", self.address)
            self.old_client=str(self.client)
            print("New client")
            numclient+=1 #Add 1 to keep track of clients
            self.chatting=True #Now Chatting
            Thread(name='server-send client:'+str(numclient), target=server.send, args=(self.client,), daemon=True).start()     #Start thread to send data to client
            Thread(name='server-receive client:'+str(numclient), target=server.receive, args=(self.client,), daemon=True).start()   #Start thread to recieve data from client

    def disconnect(self,client):
        self.client.sendall("%disconnect%".encode('utf-8'))     #Send disconnect
        s.close() #close socket
        print("Disconnected")
        self.chatting=False #No longer Chatting
        run=False

    def send(self,client):
        if self.chatting==True: #While chatting
            while self.chatting==True:
                # Send data to client in utf-8
                reply = input("\nSend :")
                reply=str(reply)
                if reply =="Q":
                    self.disconnect(client)
                else:
                    client.sendall( reply.encode('utf-8') ) # Make sure data gets there with sendall()
        else:
            sleep(2)
            self.send() #Call it's self to handle new connections

    def receive(self,client):
        if self.chatting==True: #While chatting
            print("type Q to quit")
            # Receive data and decode using utf-8
            while self.chatting == True:
                data = self.client.recv( 4096 ).decode( 'utf-8' )
                if data != None:
                    if data =="%disconnect%":
                        self.disconnect()
                    else:
                        lock = threading.Lock()
                        lock.acquire()
                        print("\nRecieved :", repr(data))
                        lock.release()
        else:
            sleep(2)
            self.receive() #Call it's self to handle new connections

server=server()
server.start()
#server.connections()
connections = Thread(name='server-connections', target=server.connections)
connections.setDaemon(True)
connections.start()
while run==True:
    pass
