from socket import *
from threading import *
socketholder = socket(AF_INET,SOCK_STREAM)
def exec_client(IP):
    global socketholder
    socketholder.connect((IP,34567))
    a = Thread(target=send_client)
    b = Thread(target=recv_client)
    a.start()
    b.start()
def send_client():
    global socketholder
    while True:
        msg = input('')
        socketholder.send(msg.encode(encoding='utf-8', errors='strict'))

def recv_client():
    global socketholder
    while True:
        data = socketholder.recv(4096).decode(encoding='utf-8', errors='strict')
        print(data)

exec_client('10.193.146.168')
