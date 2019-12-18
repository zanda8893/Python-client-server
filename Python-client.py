import socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Create socket and connect it to server
def connect():
    s.connect(('localhost',8019))
connect()
# client loop
while True:
    message = input("Your Message: ")
    s.send( message.encode('utf-8') )
    print("Awaiting the reply...")
    reply = s.recv( 1024 ).decode( 'utf-8' )
    print("Recieved ", str(reply))
