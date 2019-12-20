from threading import Thread
from time import sleep
string="thread "
def thread(string):
    while True:
        sleep(1)
        print(string+"0")
def thread1(string):
    while True:
        sleep(1)
        print(string+"1")

t1 = Thread(target = thread, args=(string,))
t2 = Thread(target = thread1, args=(string,))
t1.setDaemon(True)
t2.setDaemon(True)
print("Starting t1")
t1.start()
print("t1 started")
print("Starting t2")
t2.start()
print("t2 started")
while True:
    pass
