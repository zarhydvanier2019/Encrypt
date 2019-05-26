import os
import threading as th
import socket
import time
from random import randint
from subprocess import call

class OTP(th.Thread):
    ip = str(socket.gethostbyname(socket.gethostname()))
    port = randint(10000,50000)
    pad = []

    def __init__(self):
        """
        This is the One-Time pad initialize function. It reads  a text file with a malleable amount of
        integers. This pad that it reads is known as the One-Time pad and is the essence of this encryption
        method.
        """
        th.Thread.__init__(self)
        self.pad = self.makepad()
        OTP.pad = self.pad
        with open(os.path.join(os.environ['USERPROFILE'], "Desktop", "info.txt"), "w") as info:
            info.write(OTP.ip)
            info.write(" ")
            info.write(str(OTP.port))
        call([r'D:\Hack\info.bat'])
        call([r'D:\Hack\pad.bat'])



    def encrypt(self, sinput):  # ENCRYPTION FUNCTION
        """
         This is the One-Time Pad encrypt function. What it does is it allows the user to encrypt a desired message
         by taking the ASCII values of that specific message and performing the XOR operator between the ASCII value
         and the value of a text file, also known as the One-Time pad itself. This function returns the characters of
         the result in a string format.
        """
        e_message = []

        for value in range(0, len(sinput)):  # runs the loop for the amount of numbers in the list input
            (e_message).append(ord(sinput[value]) ^ int(OTP.pad[value]))  # XORS the message with the pad value
        return''.join(chr(n) for n in e_message)  # allows the new list to be written as a string

    def decrypt(self, e_message):  # DECRYPTION FUNCTION
        """
        This is the One-Time Pad decrypt function. It reverses the effects of the encrypt function by changing the
        values of the message back to its ASCII values, then running the XOR operation between it, and the text file
        also known as the One-Time pad. It then changes those characters back to their original character values. This
        function returns the characters in a user friendly string.
        """

        dmessage = ''  # initalizes a new variable
        for i in range (len(e_message)):  # runs a new loop for the number of characters in the encrypted message
            charval = chr(ord(e_message[i]) ^ int(OTP.pad[i]))  # XORS the encrypted message with the pad
            dmessage += charval  # above this line, the value was reset to characters, and variable equals that value

        return dmessage  # returns the contents of the string

    def exec(self):
        global socketHolder
        socketHolder.bind(('0.0.0.0', 65432))
        socketHolder.listen()
        connection, address = socketHolder.accept()
        socketHolder = connection
        a = th.Thread(target=self.server_recv)
        b = th.Thread(target= self.sends)
        a.start()
        b.start()
        print ("Ready!")

    def server_recv(self):
        global socketHolder
        while True:
            print(self.decrypt(socketHolder.recv(4096).decode(encoding='utf-8', errors='ignore')))

    def sends(self):
        global socketHolder
        try:
            while True:
                msg = input("")
                socketHolder.send((self.encrypt(msg)).encode(encoding='utf-8', errors='strict'))
        except Exception as e:
            print ("a %s has occured" %str(e))


    @staticmethod
    def makepad():
        with open(os.path.join(os.environ['USERPROFILE'], 'Desktop', "pad.txt"), "w") as f:
            for i in range(120):  # prints the contents of the text file
                f.write(str(randint(0, 255)))  # creates a random number
                f.write(" ")
        with open(os.path.join(os.environ['USERPROFILE'], 'Desktop', 'pad.txt'), "r") as r:
            pad = r.read()
            pad = pad.split()
        return pad


socketHolder = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

c = OTP()
c.exec()
