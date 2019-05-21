import socket
import time

def RSA_send(IP):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        server.connect((IP, 15432))
        server.send(bytes("bridgebuilder", encoding='utf-8'))
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        server.bind(("0.0.0.0", 6433))
        server.listen()
        connection, address = server.accept()
        with connection:
            key=(connection.recv(4096).decode(encoding='utf-8', errors='ignore')).split(" ")
            key[0], key[1] = int(key[0]), int(key[1])
        server.close()
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sender:
            time.sleep(2)
            sender.connect((IP, 15444))
            message = input("Send:")
            for n in message:  # runs for loop for length of message
                sender.send(bytes((str(((ord(n))**(key[0]))%key[1])), encoding= 'utf-8'))
            sender.send(bytes("hello", encoding='utf-8'))
        sender.close()
RSA_send('10.193.146.168')