import socket
class client():
    def __init__(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Create s and connect it to server
    def connect(self):
        self.s.connect(('localhost',8019))
        self.chatting=True
        print("Connected to server")
        return self.chatting
    def disconnect(self):
        self.s.send( "%disconnect%".encode('utf-8') ) # send disconnect message to client
        self.s.close() # close socket
        print("Disconnect from server \nPress anykey to exit") # Tell user about discconnect
    # client loop
    def chat(self):
        while self.chatting==True: #While chatting
            print("type Q to quit")
            message = input("Your Message: ")
            if message =="Q":
                self.disconnect() #disconnect
                self.chatting=False #No longer chatting
            else:
                self.s.send( message.encode('utf-8') ) # send message encode with utf-8
                print("Awaiting the reply...")
                reply = self.s.recv( 1024 ).decode( 'utf-8' ) # Receive message decode with utf-8
                if reply =="%disconnect%": # If client disconnects
                    self.disconnect() # Disconnect
                    print("Server disconnected")
                    chatting=False # no longer chatting
                else:
                    print("Recieved ", str(reply)) # print recieved message
client = client()
client.connect()
client.chat()
