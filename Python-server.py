from time import sleep
from threading import Thread
import socket
global run
run=True
s= socket.socket(socket.AF_INET, socket.SOCK_STREAM)
class server():
    def __init__(self):
        self.chatting = False
    def start(self):
        HOST = 'localhost'
        PORT = 8019
        s.bind((HOST, PORT))
        s.listen(5) # Number of connections
        print("Server started")
    def connections(self):
        while True:
            # Accept connections
            self.client, self.address = s.accept()
            print("Connected to", self.address)
            if self.client != None:
                self.chatting=True
    def disconnect(self):
        self.client.sendall("%disconnect%".encode('utf-8'))
        s.close()
        print("Disconnected")
        self.chatting=False
        run=False
    def send(self):
        while self.chatting==True:
            # Send data to client in utf-8
            reply = input("Reply :")
            reply=str(reply)
            if reply =="Q":
                self.disconnect()
            else:
                self.client.sendall( reply.encode('utf-8') ) # Make sure data gets there with sendall()
    def receive(self):
        print("type Q to quit")
        # Receive data and decode using utf-8
        while self.chatting == True:
            data = self.client.recv( 4096 ).decode( 'utf-8' )
            if data != None:
                if data =="%disconnect%":
                    self.disconnect()
                else:
                    print("Recieved :", repr(data))
server=server()
server.start()
#server.connections()
connections = Thread(name='server-connections', target=server.connections)
send = Thread(name='server-send', target=server.send)
receive = Thread(name='server-receive', target=server.receive)
send.setDaemon(True)
receive.setDaemon(True)
send.start()
receive.start()
while run==True:
    pass
