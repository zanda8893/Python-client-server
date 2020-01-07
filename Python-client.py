from time import sleep
from threading import Thread
import socket
import datetime as datetime
from tkinter import *

#global varaibles
global run
global message
run=True

class client():
    def __init__(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.count = 0
        self.log = open("Chat_log","a")

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

    def send(self):
        global message
        #print("running")
        if self.count ==0:
            self.count+=1
        msg = message.get()
        msg = str(msg)
        self.log.writelines("\n"+repr(datetime.time())+" : sent: "+msg)
        if msg =="Q":
            self.disconnect() #disconnect
        else:
            self.s.send( msg.encode('utf-8') ) # send message encode with utf-8

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
class gui():

    def __init__(self):
        pass

    def login(self):
        lgnwindow = Tk()
        #Window settings
        lgnwindow.title("Python Messenger")
        lgnwindow.geometry('256x144')
        #End windows settings
        #Text
        lbl = Label(lgnwindow, text="Enter message to send:")
        lbl.grid(column=0, row=0)
        #End Text
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
        btn = Button(window, text="Send", command=client.send)
        btn.grid(column=0, row=2)
        #End Button
        #Msg list
        listbox = Listbox(window, height=15, width=50)
        listbox.grid(column=1,row=0)
        #End msg list
        window.mainloop()

client = client()
gui = gui()
#client.connect()
#Thread(name='client-receive', target=client.receive, daemon=True).start()
#gui.messaging()
gui.login()
while run== True:
    pass
