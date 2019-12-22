from time import sleep
from threading import Thread
import socket
global run


run=True
class client():
    def __init__(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.count = 0
        # Create s and connect it to server
    def connect(self):
        loop = True
        while loop == True:
            ip = raw_input("input ip or domain name ")
            try:
                ip = socket.gethostbyname(ip)
                loop = False
            except:
                pass
        self.s.connect((ip,8019))
        self.chatting=True # Now Chatting
        print("Connected to server")

    def disconnect(self):
        global chatting
        global run
        self.s.send( "%disconnect%".encode('utf-8') ) # send disconnect message to client
        self.s.close() # close socket
        self.chatting=False # no longer chatting
        print("Disconnect from server \nPress anykey to exit") # Tell user about discconnect
        run=False

    def send(self):
        while self.chatting==True:
            #print("running")
            if self.count ==0:
                print("type Q to quit")
                self.count+=1
            message = input("\nYour Message: ")
            if message =="Q":
                self.disconnect() #disconnect
            else:
                self.s.send( message.encode('utf-8') ) # send message encode with   utf-8

    def receive(self):
        while self.chatting==True:
            #print("Test")
            reply = self.s.recv( 4096 ).decode( 'utf-8' ) # Receive message decode with utf-8
            if reply =="%disconnect%": # If client disconnects
                self.disconnect() # Disconnect
            else:
                print("\nRecieved ", str(reply)) # print recieved message

    def login(self):
        login = False
        while login == True:
            reply = False
            response = ""
            print("enter or details or type Q to quit")
            message = input("\nYour username: ")
            message2 = input("\nYour password: ")
            if message =="Q" or message2 == "Q":
                self.disconnect() #disconnect
                login = False
            else:
                self.s.send( message.encode('utf-8') ) # send message encode with   utf-8
                self.s.send( message2.encode('utf-8') ) # send message encode with   utf-8
            while reply == False:
                response = self.s.recv( 4096 ).decode( 'utf-8' ) # Receive message decode with utf-8
                if response != "":
                    reply = True
                    if response == True:
                        login = True
                    else:
                        print("incorrect details\n please try again")


client = client()
client.login()
client.connect()
Thread(name='client-send', target=client.send, daemon=True).start()
Thread(name='client-receive', target=client.receive, daemon=True).start()
while run== True:
    pass
