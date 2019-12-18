import socket
from time import sleep
s= socket.socket(socket.AF_INET, socket.SOCK_STREAM)
connected=False
class server():
    def serverstart(self):
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
            return True
    def disconnect(self):
        client.sendall("%disconnect%".encode('utf-8'))
        s.close()
        print("Disconnected")
    def chat(self):
        # Receive data and decode using utf-8
        data = client.recv( 1024 ).decode( 'utf-8' )
        if data != None:
            if data =="%disconnect%":
                self.disconnect()
                print("Server disconnected")
                connected=False
            else:
                print("Recieved :", repr(data))
                # Send data to client in utf-8
                reply = input("Reply :")
                reply=str(reply)
                client.sendall( reply.encode('utf-8') ) # Make sure data gets there with sendall()
server=server()
server.serverstart()
while connected==False:
    connected=server.connect()
if connected==True:
    while connected==True:
        sleep(0.1)
        server.chat()
