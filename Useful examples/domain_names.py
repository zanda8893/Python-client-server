import socket
#generally you loop this program

ip = input("input ip or domain name ")# idk why it wont let me use input() so im using raw_input()
#i think it is my ide being quirky and running the wrong version of python
try:
    ip = socket.gethostbyname(ip)
except:
    pass
print(ip)
