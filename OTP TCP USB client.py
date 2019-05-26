import threading as t
import socket
import time
import os
def decrypt(e_message, pad = open(os.path.join('D:\pad.txt')).read().split(" ")):  # DECRYPTION FUNCTION
    """
    This is the One-Time Pad decrypt function. It reverses the effects of the encrypt function by changing the
    values of the message back to its ASCII values, then running the XOR operation between it, and the text file
    also known as the One-Time pad. It then changes those characters back to their original character values. This
    function returns the characters in a user friendly string.
    """

    dmessage = ''  # initalizes a new variable
    for i in range(len(e_message)):  # runs a new loop for the number of characters in the encrypted message
        charval = chr(ord(e_message[i]) ^ int(pad[i]))  # XORS the encrypted message with the pad
        dmessage += charval  # above this line, the value was reset to characters, and variable equals that value

    return dmessage  # returns the contents of the string

def encrypt( sinput, pad = open(os.path.join('D:\pad.txt')).read().split(" ")):
    """
         This is the One-Time Pad encrypt function. What it does is it allows the user to encrypt a desired message
         by taking the ASCII values of that specific message and performing the XOR operator between the ASCII value
         and the value of a text file, also known as the One-Time pad itself. This function returns the characters of
         the result in a string format.
        """
    e_message = []

    for value in range(0, len(sinput)):  # runs the loop for the amount of numbers in the list input
        (e_message).append(ord(sinput[value]) ^ int(pad[value]))  # XORS the message with the pad value
    return''.join(chr(n) for n in e_message)  # allows the new list to be written as a string


def server_recv():
    global socketHolder
    while True:
        data = (decrypt(socketHolder.recv(4096).decode(encoding = 'utf-8', errors='strict')))
        if data:
            print(data)
            return data



def send():
    global socketHolder
    while True:
        msg = input("")
        socketHolder.send((encrypt(msg)).encode(encoding='utf-8', errors='strict'))




class thread(t.Thread):
    def __init__(self) :
        t.Thread.__init__(self)
    def exec(self):
        global socketHolder, IPtuple
        socketHolder.connect(IPtuple)
        a = t.Thread(target=server_recv)
        b = t.Thread(target= send)
        b.start()
        a.start()

info = open(os.path.join('D:\info.txt')).read().split(" ")
socketHolder = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
IPtuple = ((str(info[0]), 65432))


a = thread()
a.exec()
print("Connected!")

