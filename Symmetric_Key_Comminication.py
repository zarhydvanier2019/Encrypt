from socket import *
from threading import *
socketHolder = socket(AF_INET, SOCK_STREAM)
def Communicate(self,sender=True, IP='0.0.0.0'):
    global socketHolder 
    if sender:
        socketHolder.connect((IP, 54321))
        print ("connected")
    else:
        socketHolder.bind(('0.0.0.0', 54321))
        socketHolder.listen()
        connection, address = socketHolder.accept()
        socketHolder = connection

    a = Thread(target=self.sends)
    b = Thread(target=self.recv)

def sends(self):
    global socketHolder #call variable as global
    while True:
        msg = input("") #placeholder for a way fof getting input
        socketHolder.send((msg).encode(encoding='utf-8', errors='ignore')) #sends input(add your encryption here)

def recv(self):
    global socketHolder #call variable as global
    while True:
        data = socketHolder.recv(4096).decode(encoding = 'utf-8', errors='strict') #recieves data from connection
        print(data) #put decryption function here
