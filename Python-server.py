from time import sleep
from threading import Thread
import threading
import socket
import sqlite3
import getpass
global run
#global varaibles
run=True
s= socket.socket(socket.AF_INET, socket.SOCK_STREAM) #Define parameters for socket connection
class server():

    def __init__(self):
        self.chatting = False #Not Chatting
        self.old_client=0
        self.dbsetup()

    def dbsetup(self):
        self.db = sqlite3.connect("Server.db")
        self.cursor=self.db.cursor()
        self.cursor.execute(""" CREATE TABLE IF NOT EXISTS Users(
        id integer PRIMARY KEY,
        username text NOT NULL,
        passwords text NOT NULL); """)
        self.db.commit()
        self.cursor.close()

    def start(self):
        HOST = 'localhost'
        PORT = 8019
        s.bind((HOST, PORT)) #bind port and host
        s.listen(5) # Number of connections in backlog
        print("Server started")

    def connections(self):
        numclient=0 # set the number of clients to zero
        while True:
            self.client, self.address = s.accept() # Accept connections
            print("Connected to", self.address,"+",self.client)
            self.old_client=str(self.client)
            print("New client")
            numclient+=1 #Add 1 to keep track of clients
            self.chatting=True #Now Chatting
            clientname = self.login(self.client)
            clientdata = [clientname,self.client]
            #Thread(name='server-send client:'+str(clientname), target=server.send, args=(self.client,), daemon=True).start()     #Start thread to send data to client
            Thread(name='server-receive client:'+str(clientname), target=server.receive, args=(clientdata,), daemon=True).start()   #Start thread to recieve data from client

    def login(self,client):
        print("Running login")
        correctuser = False
        correctpassword = False
        self.db = sqlite3.connect("Server.db")
        self.cursor=self.db.cursor()
        login = False
        client.sendall( "%login%".encode('utf-8') )
        while login==False:
            userinfo = self.client.recv( 4096 ).decode( 'utf-8' )
            if userinfo != None:
                userinfo = userinfo.split()
                username = userinfo[0]
                password = userinfo[1]
                self.cursor.execute("SELECT username FROM Users WHERE username=?", (username,))
                usersql = self.cursor.fetchall()
                for row in usersql:
                    if row == username:
                        correctuser=True
                self.cursor.execute("SELECT passwords FROM Users WHERE passwords=?", (password,))
                usersql = self.cursor.fetchall()
                for row in usersql:
                    if row == password:
                        correctpassword = True
                if correctuser and correctpassword ==True:
                    print("Logged in")
                self.cursor.close()
                userinfo = None
                if login ==True:
                    self.chatting=True
                    return username

    def disconnect(self,client):
        self.client.sendall("%disconnect%".encode('utf-8'))     #Send disconnect
        s.close() #close socket
        print("Disconnected")
        self.chatting=False #No longer Chatting
        run=False

    def send(self,client,msg):
        client.sendall( msg.encode('utf-8') ) # Make sure data gets there with sendall()

    def receive(self,clientdata):
        clientdata = clientdata.split()
        sclient = clientdata[0]
        username = clientdata[1]
        while self.chatting == True:
            data = sclient.recv( 4096 ).decode( 'utf-8' )
            if data != None:
                if data =="%disconnect%":
                    self.disconnect()
                    self.chatting = False
                else:
                    data = data.split()
                    who = data[0]
                    msg = data[1]
                    rclient = user_search(who)
                    if rclient = 0:
                        self.send(sclient,"User not logged in")
                    else:
                        self.send(rclient,msg)

    def user_search(self,username):
        if username in self.users:
            nameloc = self.users.index(username)
            clientloc = namelocation+1
            client = self.users[clientloc]
            return client
        else:
            return 0

    def addusers(self):
        self.db = sqlite3.connect("Server.db")
        self.cursor=self.db.cursor()
        name = input("Enter username:")
        password = getpass.getpass(prompt='Password: ', stream=None)
        self.cursor.execute(""" INSERT INTO Users(username,passwords)
        VALUES (?,?)""",(name,password))
        self.db.commit()
        self.cursor.close()

server=server()
server.start()
Thread(name='server-connections', target=server.connections, daemon=True).start()
while run==True:
    pass
#server.addusers()
