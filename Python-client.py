import socket
class server():
    def __init__(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Create s and connect it to server
    def connect(self):
        self.s.connect(('localhost',8019))
    def dissconnect(self):
        self.s.close()
    # client loop
    def chat():
        while True:
            message = input("Your Message: ")
            s.send( message.encode('utf-8') )
            print("Awaiting the reply...")
            reply = s.recv( 1024 ).decode( 'utf-8' )
            if reply =="%disconect%":
                dissconnect()
                print("Server dissconnected")
            else:
                print("Recieved ", str(reply))
server.s.connect()
