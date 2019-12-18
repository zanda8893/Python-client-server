import socket
from time import sleep
s= socket.socket(socket.AF_INET, socket.SOCK_STREAM)
connected=False
def serverstart():
    HOST = 'localhost'
    PORT = 8019
    s.bind((HOST, PORT))
    s.listen(5) # Number of connections

def connect():
    global client #global varables to be used in chat()
    global address
    # Accept connections
    client, address = s.accept()
    print("Connected to", address)
    if client != None:
        return True
def dissconnect():
    dis="%disconect%"
    client.sendall(dis.enode('utf-8'))
def chat():
    # Receive data and decode using utf-8
    data = client.recv( 1024 ).decode( 'utf-8' )
    if data != None:
        print("Recieved :", repr(data))

        # Send data to client in utf-8
        reply = input("Reply :")
        reply=str(reply)
        client.sendall( reply.encode('utf-8') ) # Make sure data gets there with sendall()

serverstart()
while connected==False:
    connected=connect()
if connected==True:
    while True:
        sleep(1)
        chat()
