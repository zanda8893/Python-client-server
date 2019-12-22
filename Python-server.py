from time import sleep
from threading import Thread
import socket
global run
import json #needed later
import sqlite3 as sql #for the logging in

run=True
s= socket.socket(socket.AF_INET, socket.SOCK_STREAM)

class server():
    def __init__(self):
        self.chatting = False
        self.old_client=0
    def start(self):
        loop = True
        while loop == True:
            ip = raw_input("input ip or domain name ")
            try:
                ip = socket.gethostbyname(ip)
                loop = False
            except:
                pass
        PORT = 8019
        s.bind((ip, PORT))
        s.listen(5) # Number of connections
        print("Server started")
    def connections(self):
        numclient=0 # set the number of clients to zero
        while True:
            self.client, self.address = s.accept() # Accept connections
            print("Connected to", self.address)
            self.old_client=str(self.client)
            print("New client")
            self.old_client=str(self.client)
            numclient+=1
            self.chatting=True
            self.authenticate()
            Thread(name='server-send client:'+str(numclient), target=server.send, args=(self.client,), daemon=True).start()
            Thread(name='server-receive client:'+str(numclient), target=server.receive, args=(self.client,), daemon=True).start()

    def disconnect(self,client):
        self.client.sendall("%disconnect%".encode('utf-8'))
        s.close()
        print("Disconnected")
        self.chatting=False
        run=False

    def send(self,client):
        if self.chatting==True:
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
            self.send()

    def receive(self,client):
        if self.chatting==True:
            print("type Q to quit")
            # Receive data and decode using utf-8
            while self.chatting == True:
                data = self.client.recv( 4096 ).decode( 'utf-8' )
                if data != None:
                    if data =="%disconnect%":
                        self.disconnect()
                    else:
                        print("\nRecieved :", repr(data))
        else:
            sleep(2)
            self.receive()

    def authenticate(self,client):
        login = False
        if self.chatting!=True:
            # Receive data and decode using utf-8
            while self.chatting == True and login == False:
                data = self.client.recv( 4096 ).decode( 'utf-8' )
                data2 = self.client.recv( 4096 ).decode( 'utf-8' )
                if data != None:
                    if data =="%disconnect%":
                        self.disconnect()
                    else:
                        username = repr(data)
                        password = repr(data2)
                        #sql database comaprison there
                        #temp filler
                        if username == 'username' and password == 'password':
                            reply = True
                            login = True
                            client.sendall( reply.encode('utf-8') )
                        else:
                            reply = False
                            client.sendall( reply.encode('utf-8') )
        else:
            sleep(2)
            self.receive()
        #pull sql code from other program for logins
server=server()
server.start()
#server.connections()
connections = Thread(name='server-connections', target=server.connections)
connections.setDaemon(True)
connections.start()
while run==True:
    pass
