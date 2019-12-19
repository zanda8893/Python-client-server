import socket
import threading
class client():
    def __init__(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.count = 0
        # Create s and connect it to server
    def connect(self):
        global chatting
        self.s.connect(('localhost',8019))
        chatting=True # Now Chatting
        print("Connected to server")
    def disconnect(self):
        self.s.send( "%disconnect%".encode('utf-8') ) # send disconnect message to client
        self.s.close() # close socket
        chatting=False # no longer chatting
        print("Disconnect from server \nPress anykey to exit") # Tell user about discconnect
    def send(self):
        if self.count ==0:
            print("type Q to quit")
            self.count+=1
        message = input("Your Message: ")
        if message =="Q":
            self.disconnect() #disconnect
        else:
            self.s.send( message.encode('utf-8') ) # send message encode with utf-8
    def receive(self):
            reply = self.s.recv( 1024 ).decode( 'utf-8' ) # Receive message decode with utf-8
            if reply =="%disconnect%": # If client disconnects
                self.disconnect() # Disconnect
                print("Server disconnected")
            else:
                print("Recieved ", str(reply)) # print recieved message
client = client()
print(threading.active_count())

client.connect()
while chatting==True:
    client.send()
    client.receive()
