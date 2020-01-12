from time import sleep
from threading import Thread
import socket
import datetime as datetime
from tkinter import *
from functools import partial
#global varaibles
global run
global message
run=True

class client():
    def __init__(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.count = 0
        self.log = open("Chat_log","a")
        self.gui = gui()

    def connect(self):
        self.s.connect(('localhost',8019))
        self.chatting=True # Now Chatting
        print("Connected to server")
        self.log.writelines("\n       *****"+repr(datetime.datetime.now())+"*****       \n")  #Write current date and time to file

    def disconnect(self):
        global chatting
        global run
        self.s.send( "%disconnect%".encode('utf-8') ) # send disconnect message to client
        self.s.close() # close socket
        self.chatting=False # no longer chatting
        print("Disconnect from server \nPress anykey to exit") # Tell user about discconnect
        self.log.close()
        run=False

    def send(self,msg):
        msg = str(msg)
        if msg == "gui":
            msg = message.get()
        self.log.writelines("\n"+repr(datetime.time())+" : sent: "+msg)
        if msg =="Q":
            self.disconnect() #disconnect
        else:
            self.s.send( msg.encode('utf-8') ) # send message encode with utf-8
            print(msg)

    def receive(self):
        while self.chatting==True:
            #print("Test")
            reply = self.s.recv( 4096 ).decode( 'utf-8' ) # Receive message decode with utf-8
            self.log.writelines("\n"+repr(datetime.time())+" : received: "+reply)
            reply = str(reply)
            if reply =="%disconnect%": # If client disconnects
                self.disconnect() # Disconnect
            else:
                print("\nRecieved ", reply) # print recieved message
                lstbox=gui.messaging.listbox
                lstbox.insert(END, reply)

    def login(self):
        global username
        global password
        username = username.get()
        password = password.get()
        user = (str(username)+" "+str(password))
        self.send(user)

class gui():

    def __init__(self):
        pass

    def login(self):
        global username
        global password
        lgnwindow = Tk()
        #Window settings
        lgnwindow.title("Python Messenger")
        lgnwindow.geometry('256x144')
        #End windows settings
        #Text
        lbluser = Label(lgnwindow, text="Username:")
        lbluser.grid(column=0, row=0)
        lblpass = Label(lgnwindow, text="Password:")
        lblpass.grid(column=0, row=1)
        #End Text
        #Text entry
        username = Entry(lgnwindow, width=10)
        password = Entry(lgnwindow, width=10)
        username.grid(column=1, row=0)
        password.grid(column=1, row=1)
        #Button
        #sendlogin = client.login(username,password)
        btn = Button(lgnwindow, text="Login", command=client.login)
        btn.grid(column=3, row=0)
        #End Button
        lgnwindow.mainloop()

    def chat_select(self):
        chatwindow = Tk()
        #Window settings
        chatwindow.title("Chat select")
        chatwindow.geometry("576x324")
        #End window settings
        #text
        lblchat = Label(chatwindow, text="Select chat:").grid(column=0, row=0)
    def messaging(self):
        global message
        window = Tk()
        #Window settings
        window.title("Python Messenger")
        window.geometry('640x360')
        #End windows settings
        #Text
        lbl = Label(window, text="Enter message to send:")
        lbl.grid(column=0, row=0)
        #End Text
        #Text entry
        message = Entry(window,width=10)
        message.grid(column=0,row=1)
        #End text entry
        #Button
        btn = Button(window, text="Send", command=partial(client.send,"gui"))
        btn.grid(column=0, row=2)
        #End Button
        #Msg list
        listbox = Listbox(window, height=15, width=50)
        listbox.grid(column=1,row=0)
        #End msg list
        window.mainloop()

client = client()
gui = gui()
client.connect()
#Thread(name='client-receive', target=client.receive, daemon=True).start()
gui.login()
while run== True:
    pass
