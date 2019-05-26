from socket import *
from threading import *
# all regular methods NOT STATIC
socketHolder = socket(AF_INET, SOCK_STREAM) #this is a global variable, so it will be called as such in each method
def exec():
    global socketHolder #call variable as global
    socketHolder.bind(('0.0.0.0', 34567))   #binds socket to communicate on
    socketHolder.listen()
    connection, address = socketHolder.accept() #accepts connection from other computer, splitting into address and socket object
    socketHolder = connection #updates the default socket object to the connection object
    print("Connected to %s on port %i" %(address[0], address[1])) #prints IP address and port of connector
    a = Thread(target=sends)    #creates threads to send and recieve and starts them
    b = Thread(target=recv)
    a.start()
    b.start()

def sends():
    global socketHolder #call variable as global
    while True:
        msg = input("") #placeholder for a way fof getting input
        socketHolder.send((msg).encode(encoding='utf-8', errors='ignore')) #sends input(add your encryption here)

def recv():
    global socketHolder #call variable as global
    while True:
        data = socketHolder.recv(4096).decode(encoding = 'utf-8', errors='strict') #recieves data from connection
        if data: #if the data is not null(i.e something was sent) the data is returned and printed
            print(data) #put decryption function here
            return data
