import socket
from time import sleep
s= socket.socket(socket.AF_INET, socket.SOCK_STREAM)
connected=False
class server():
    def __init__(self):
        self.start()
        self.connect()
        self.chat()
    def start(self):
        HOST = 'localhost'
        PORT = 8019
        s.bind((HOST, PORT))
        s.listen(5) # Number of connections
        print("Server started")
    def connect(self):
        global client #global varables to be used in chat()
        global address
        # Accept connections
        client, address = s.accept()
        print("Connected to", address)
        if client != None:
            self.chatting=True
    def disconnect(self):
        client.sendall("%disconnect%".encode('utf-8'))
        s.close()
        print("Disconnected")
        self.chatting=False
        self.__init__()
    def chat(self):
        print("type Q to quit")
        # Receive data and decode using utf-8
        while self.chatting == True:
            data = client.recv( 1024 ).decode( 'utf-8' )
            if data != None:
                if data =="%disconnect%":
                    self.disconnect()
                else:
                    print("Recieved :", repr(data))
                    # Send data to client in utf-8
                    reply = input("Reply :")
                    reply=str(reply)
                    if reply =="Q":
                        self.disconnect()
                    else:
                        client.sendall( reply.encode('utf-8') ) # Make sure data gets there with sendall()
server()
