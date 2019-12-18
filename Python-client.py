import socket
class server():
    def __init__(self)
    self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Create socket and connect it to server
    def connect():
        self.socket.connect(('localhost',8019))
    def dissconnect():
        self.socket.close()
    # client loop
    while True:
        message = input("Your Message: ")
        self.socket.send( message.encode('utf-8') )
        print("Awaiting the reply...")
        reply = self.socket..recv( 1024 ).decode( 'utf-8' )
        if reply =="%disconect%":
            dissconnect()
            print("Server dissconnected")
        else:
            print("Recieved ", str(reply))
server.socket.connect()
