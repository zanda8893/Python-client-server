#!/usr/bin/python3
from threading import Thread
import socket
import datetime
from tkinter import Tk, Label, Entry, Button, Listbox


#global varaibles
global run
global gui
run = True

class client():
    def __init__(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.count = 0
        self.log = open("Chat_log", "a")
        self.chatting = False

    def connect(self):
        self.s.connect(('localhost', 8019))
        self.chatting = True # Now Chatting
        print("Connected to server")
        self.log.writelines("\n       *****"+repr(datetime.datetime.now())+ \
        "*****       \n")  #Write current date and time to file

    def disconnect(self):
        global chatting
        global run
        self.s.send("%disconnect%".encode('utf-8')) #Send disconnect message to client
        self.s.close() # close socket
        self.chatting = False # no longer chatting
        print("Disconnect from server \nPress anykey to exit") # Tell user about discconnect
        self.log.close()
        run = False

    def send(self, msg):
        self.log.writelines("\n"+repr(datetime.time())+" : sent: "+msg)
        if msg == "Q":
            self.disconnect() #disconnect
        else:
            self.s.send(msg.encode('utf-8')) #Send message encode with utf-8

    def receive(self):
        while self.chatting:
            #print("Test")
            reply = self.s.recv(4096).decode('utf-8') #Receive message decode with utf-8
            self.log.writelines("\n"+repr(datetime.time())+" : received: "+reply)
            reply = str(reply)
            if reply == "%disconnect%": # If client disconnects
                self.disconnect() # Disconnect
            else:
                global gui
                print("Got ", reply)
                gui.listbox.insert(END, reply)

class gui():
    def __init__(self):
        self.client = client()
        self.client.connect()
        self.window = Tk()
        #Window settings
        self.window.title("Python Messenger")
        self.window.geometry('500x500')
        #Text
        lbl = Label(self.window, text="Enter message to send:")
        lbl.grid(column=0, row=1)
        #Text entry
        self.message = Entry(self.window, width=30)
        self.message.grid(column=0, row=2)
        #Button
        btn = Button(self.window, text="Send", command=self.sendmsg)
        btn.grid(column=1, row=2)
        #Msg list
        self.listbox = Listbox(self.window, height=15, width=50)
        self.listbox.grid(column=0, row=0)

    def sendmsg(self):
        self.client.send(str(self.message.get()))

    def login(self):
        pass

    def mainloop(self):
        Thread(name='client-receive', target=self.client.receive, daemon=True).start()
        self.window.mainloop()

gui = gui()
gui.mainloop()
while run:
    pass
