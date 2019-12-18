import socket
class server():
    def __init__(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Create s and connect it to server
    def connect(self):
        self.s.connect(('localhost',8019))
        chatting==True
        print("Connected to server")
        return chatting
    def dissconnect():
        self.s.close()
    # client loop
    def chat():
        while chatting==True:
            print("type Q to quit")
            message = input("Your Message: ")
            if message =="Q":
                dissconnect()
                chatting=False
            else:
                s.send( message.encode('utf-8') )
                print("Awaiting the reply...")
                reply = s.recv( 1024 ).decode( 'utf-8' )
                if reply =="%disconect%":
                    dissconnect()
                    print("Server dissconnected")
                    chatting=False
                else:
                    print("Recieved ", str(reply))
server = server()
chatting=server.connect(self)
sleep(1)
server.chat()
