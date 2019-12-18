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
        self.s.send( "%disconnect%".encode('utf-8') )
        self.s.close()
        print("Disconnect from server \nPress anykey to exit")
    # client loop
    def chat(self):
        while self.chatting==True:
            print("type Q to quit")
            message = input("Your Message: ")
            if message =="Q":
                self.disconnect()
                self.chatting=False
            else:
                self.s.send( message.encode('utf-8') )
                print("Awaiting the reply...")
                reply = self.s.recv( 1024 ).decode( 'utf-8' )
                if reply =="%disconect%":
                    self.disconnect()
                    print("Server disconnected")
                    chatting=False
                else:
                    print("Recieved ", str(reply))
client = client()
client.connect()
client.chat()
