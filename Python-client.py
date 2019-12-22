from time import sleep
from threading import Thread
import socket
import datetime as datetime
global run
#global varaibles

run=True

class client():
    def __init__(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.count = 0
        self.log = open("Chat_log","a")
        # Create s and connect it to server

    def connect(self):
        self.s.connect(('localhost',8019))
        self.chatting=True # Now Chatting
        print("Connected to server")
        self.log.writelines("\n       *****"+repr(datetime.datetime.now())+"*****       \n")  #Write current date and time to file

    def disconnect(self):
        global chatting
        global run
        self.s.send( "%disconnect%".encode('utf-8') ) # send disconnect message to client
        self.s.close() # close socket
        self.chatting=False # no longer chatting
        print("Disconnect from server \nPress anykey to exit") # Tell user about discconnect
        self.log.close()
        run=False

    def send(self):
        while self.chatting==True:
            #print("running")
            if self.count ==0:
                print("type Q to quit")
                self.count+=1
            message = input("\nYour Message: ")
            self.log.writelines("\n"+repr(datetime.time())+" : sent: "+message)
            if message =="Q":
                self.disconnect() #disconnect
            else:
                self.s.send( message.encode('utf-8') ) # send message encode with utf-8

    def receive(self):
        while self.chatting==True:
            #print("Test")
            reply = self.s.recv( 4096 ).decode( 'utf-8' ) # Receive message decode with utf-8
            self.log.writelines("\n"+repr(datetime.time())+" : received: "+reply)
            if reply =="%disconnect%": # If client disconnects
                self.disconnect() # Disconnect
            else:
                print("\nRecieved ", str(reply)) # print recieved message

client = client()
client.connect()
Thread(name='client-send', target=client.send, daemon=True).start()
Thread(name='client-receive', target=client.receive, daemon=True).start()
while run== True:
    pass
