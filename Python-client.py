from time import sleep
from threading import Thread
import socket

class client():
    def __init__(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.count = 0
        # Create s and connect it to server
    def connect(self):
        self.s.connect(('localhost',8019))
        self.chatting=True # Now Chatting
        print("Connected to server")
    def disconnect(self):
        global chatting
        self.s.send( "%disconnect%".encode('utf-8') ) # send disconnect message to client
        self.s.close() # close socket
        self.chatting=False # no longer chatting
        print("Disconnect from server \nPress anykey to exit") # Tell user about discconnect
    def send(self):
        while self.chatting==True:
            #print("running")
            if self.count ==0:
                print("type Q to quit")
                self.count+=1
            message = input("Your Message: ")
            if message =="Q":
                self.disconnect() #disconnect
            else:
                self.s.send( message.encode('utf-8') ) # send message encode with utf-8
    def receive(self):
        while self.chatting==True:
            #print("Test")
            reply = self.s.recv( 1024 ).decode( 'utf-8' ) # Receive message decode with utf-8
            if reply =="%disconnect%": # If client disconnects
                self.disconnect() # Disconnect
            else:
                print("\nRecieved ", str(reply)) # print recieved message
client = client()
client.connect()
send = Thread(name='client-send', target=client.send)
receive = Thread(name='client-receive', target=client.receive)
send.setDaemon(True)
receive.setDaemon(True)
send.start()
receive.start()
while True:
    pass
