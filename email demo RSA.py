import random
import math
import socket
import time
import threading
MMI = lambda A, n,s=1,t=0,N=0: (n < 2 and t%N or MMI(n, A%n, t, s-A//n*t, N or n),-1)[n<1]
'''lambda (one line function) for modular multiplicative inverse of a and n, found on code signal, made by Yousef Hadder'''
class RSA:                                                                                  # credit : Yousef Hadder, Code signal
    '''Sets up the a class for an instance of rsa communication'''
    def __init__(self):
        '''
        This function initializes an RSA object, meaning all related numbers are generated, as are the keys
        The code follows this algorithm to generate the keys, and the attributes are aptly named:
        p and q are two prime numbers, generated randomly (not in a cryptographically secure way) from a list
        p and q are guarenteed to be different before continuing
        n, the modulus for both of the future keys is generated by p and q's multiplication
        the totient, number of coprimes of p and q from 1 to n found using the LCM p-1 and q-1
        e, the first part of the encryption key is generated using a number coprime with the totient and n less than the totient
        this is circumvented using
        d is generated as the modular multiplicative inverse of e and the totient
        '''
        self.numlist = [199,	211,	223,	227,	229,	233,	239,	241,	251,	257,
                        263,	269,	271,	277,	281,	283,	293,	307,	311,	313]

        # The list of primes above is used to generate prme numbers to be used in the code
        self.p = self.numlist[random.randint(0, len(self.numlist)-1)] #p is generated randomly
        self.q = self.numlist[random.randint(0, len(self.numlist)-1)] #q is generated randomly
        while self.q == self.p: # as p and q must not be equal, this runs the random selsection until different values selected
            self.q = self.numlist[random.randint(0, len(self.numlist)-1)]
        self.n = self.p * self.q #n is genrated as the product of p and q
        self.totient = (self.p - 1)*(self.q - 1)//math.gcd(self.p-1, self.q-1) #totient(n), the number of coprimes with p and q from 1 to n is genterated
        self.numlist2 = []
        for icounter in range(2, self.totient):  # counts to one past upper limit (pre conditional)
            bprime = True  # predefines each number as prime, to be disproven
            ichecker = 2  # starts checker at 2, as that is the smallest prime
            while bprime != False and ichecker < int( float(icounter ** (1 / 2) + 1)):  # allows exit when proven composite or after all test cases
                if icounter % ichecker == 0:  # checks if the mod of any number gives 0 indicating non prime
                    bprime = False  # sets prime value to false, so it is not counted in later commands
                else:
                    ichecker += 1  # ichecker moves onto next test number
            if bprime == True and self.totient%icounter != 0:
                self.numlist2.append(icounter)  # appends number
        self.e = self.numlist2[random.randint(0,len(self.numlist2))]

        #self.d = self.e*(random.randint(10,20)) #generates a random value for d, to be found valid or manipulated until it is
        self.d = MMI(self.e, self.totient) # implementation of lambda pasted outside the class

        self.encryptkey = (self.e, self.n) # generates tuple to act as lock
        self.decryptkey = (self.d, self.n) #generates tuple to act as key

    def encrypt(self, k1, k2, message):
        encrypted = []
        for letter in message:
            encrypted.append((ord(letter))**k1%k2)
        return str(' '.join(n for n in encrypted))



    def decrypt(self, emessage): #takes an encrypted message
        '''
        :param emessage: This is an encrypted message, encrypted by the respective method in this very class or the staticmethod 'send'
        :return: The decrypted emessage as a string using the keys for the instance of conversation
        '''
        ' '.split(emessage)
        decrypted = [] #creates an empty list
        for n in emessage:
            decrypted.append((int(n)**(self.decryptkey[0]))%(self.decryptkey[1])) #Decrypts ASCII value (decrypted) to list
        decrypted = "".join(str(chr(n)) for n in decrypted) #creates string from list of decrypted values and turns each ASCII to a character
        return decrypted

    def server(self):
        '''
        Creates a single client server that recieves a meaningless message, sends the public key to the client, and
        recieves an encrypted message.
        :return: The dercypted message using the decrypt method found in this class
        '''
        incoming = [] #creates an empty list to recieve the incoming encrypted characters
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server: #creates a "setup" server
            server.bind(("0.0.0.0", 15432)) #binds the socket to listen on all available networks
            server.listen() #listens for a client to connect
            connection, address = server.accept() #recieves two return values of accept() the latter will be used to send keys
            server.close() #closes the connection establishing code
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server: #sends the key as generated by init()
            server.connect((address[0], 6433))# uses pre-established address variable to get server IP
            server.send(bytes((str(self.encryptkey[0]))+" "+(str(self.encryptkey[1])), encoding='utf-8')) #sends key
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:# creates  the connection to recieve the message
            server.bind(("0.0.0.0", 15444))
            server.listen() #listens on all networks
            conn, addr = server.accept() #recieves two input from accept()
            with conn:
                length = int(conn.recv(4096).decode(encoding='utf-8', errors='strict'))
                for n in range(length):
                    incoming.append(int(conn.recv(4096).decode(encoding='utf-8', errors='strict')))
                print (incoming)
                return (self.decrypt(incoming))


    @staticmethod
    def RSA_send(IP):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
            server.connect((IP, 15432))
            server.send(bytes("bridgebuilder", encoding='utf-8'))
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
            server.bind(("0.0.0.0", 6433))
            server.listen()
            connection, address = server.accept()
            with connection:
                key = (connection.recv(4096).decode(encoding='utf-8', errors='ignore')).split(" ")
                key0 = int(key[0])
                key1 = int(key[1])
            server.close()
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sender:
                time.sleep(2)
                sender.connect((IP, 15444))
                message = input("Send:")
                sender.send(bytes(str(len(message)), encoding='utf-8'))
                for n in message:  # runs for loop for length of message
                    sender.send(bytes((str(((ord(n)) ** key0) % key1)), encoding='utf-8'))
                    time.sleep(0.05)
                sender.close()

class email(RSA, threading.Thread):
    def __init__(self):
        RSA.__init__(self)
        threading.Thread.__init__(self)
        self.IP = str(socket.gethostbyname(socket.gethostname()))
        self.address = input("Enter your new email address: ")
        self.password = input("Set your password: ")
        self.SHApass = 0 # to be determined by the SHA-256 function
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as c:
            c.connect(('10.193.146.158', 48665))
            c.send(self.address.encode(encoding= 'utf-8', errors='strict'))
            c.send(str(self.SHApass).encode(encoding='utf-8', errors='strict'))
            c.send(str(self.encryptkey[0]).encode(encoding='utf-8', errors='strict'))
            c.send(str(self.encryptkey[1]).encode(encoding='utf-8', errors='strict'))

    def send(self):
        address = input("Send to: ")
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as c:
            c.connect(('10.193.146.158', 32132))
            c.send(address.encode(encoding= 'utf-8', errors='strict'))
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as k:
            k.bind(('0.0.0.0', 87979))
            k.listen()
            conn, addr = k.accept()
            with conn:
                key1 = int(conn.recv(4096))
                key2 = int(conn.recv(4096))
            k.close()
        message = input("Message: \n")
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as c:
            c.connect(('10.193.146.158', 69797))
            c.send(self.encrypt(key1, key2, message).encode(encoding='utf-8', errors='ignore'))

    def recv(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as c:
            c.bind(('0.0.0.0', 12678))
            c.listen()
            conn, addr = c.accept()
            with conn:
                adr = conn.recv(4096).decode(encoding='utf-8', errors='strict')
                print("Recieved from:"+adr)
                msg = self.decrypt(conn.recv(4096).decode(encoding='utf-8', errors='strict'))
                print(msg)

    def runs(self, send = (input("Send a message? (1 for yes, 0 for no"))):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as c:
            c.bind(('0.0.0.0', 12678))
            c.listen()
            conn, addr = c.accept()
            with conn:
                msg_number = int((conn.recv(4096)).decode(encoding='utf-8', errors='strict'))
            c.close()
        for n in range (msg_number):
            self.recv()
        c.close()
        try:
            if int(send):
                self.send()
        except ValueError:
            print("Thank you for using email.ru")

thread1 = email()
t = threading.Thread(target=email.runs)
