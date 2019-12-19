from threading import Thread
def thread():
    while True:
        print("Thread 1")
def thread1():
    while True:
        print("Thread 2")

t1 = Thread(target = thread)
t2 = Thread(target = thread1)
t1.setDaemon(True)
t2.setDaemon(True)
t1.start()
t2.start()
while True:
    pass
