import random
import math
import socket
import time
import threading
class RSA:
    # (one line function) for modular multiplicative inverse of a and n, found on code signal, made by Yousef Hadder
    MMI = lambda A, n, s=1, t=0, N=0: (n < 2 and t % N or RSA.MMI(n, A % n, t, s - A // n * t, N or n), -1)[n < 1]
    # credit : Yousef Hadder, Code signal
    '''Sets up the a class for an instance of rsa communication
    Methods:
    self.__init__ : No paramaters, runs algorithm to create encryption and decryption keys, no return

    self.encrypt: (staticmethod)
    Parameters = exponent and modulus of the key (not necessairily the object's), message to encrypt as string
    This method takes a message as a string and returns it as a list with each characters ascii value encrypted and added to a list
    return = encrypted message as strng

    self.decrypt:
    Parameters = message to be decrypted
    This method takes an encrypted string and splits it, decrypts it and rejoins it
    return = message decrypted using the object's decrypt key
    
    self.sends:
    Parameters = the exponenet and modulus of the others public key in a connection
    this method sends messages constantly and sends them encrypted
    returns = none
    
    self.receive:
    Parameters = none
    always recieves messages, and prints them decrypted
    returns = none
    
    self.communicate:
    Parameters = boolean to determine whether to connect first of second, secod is IP, and third is port
    establishes connection, exchanges keys and starts self.sends and self.receive threads in parallel
    return = none
    '''

    def __init__(self):
        '''
        This function initializes an RSA object, meaning all related numbers are generated, as are the keys
        The code follows this algorithm to generate the keys, and the attributes are aptly named:
        p and q are two prime numbers, generated randomly (not in a cryptographically secure way) from a list
        p and q are guarenteed to be different before continuing
        n, the modulus for both of the future keys is generated by p and q's multiplication
        the totient, number of coprimes of p and q from 1 to n found using the LCM p-1 and q-1
        e, the first part of the encryption key is generated using a number coprime with the totient and n less than the totient
        d is generated as the modular multiplicative inverse of e and the totient
        '''
        self.numlist = [199, 211, 223, 227, 229, 233, 239, 241, 251, 257,
                        263, 269, 271, 277, 281, 283, 293, 307, 311, 313]

        # The list of primes above is used to generate prme numbers to be used in the code
        self.p = self.numlist[random.randint(0, len(self.numlist) - 1)]  # p is generated randomly
        self.q = self.numlist[random.randint(0, len(self.numlist) - 1)]  # q is generated randomly
        while self.q == self.p:  # as p and q must not be equal, this runs the random selsection until different values selected
            self.q = self.numlist[random.randint(0, len(self.numlist) - 1)]
        self.n = self.p * self.q  # n is genrated as the product of p and q
        self.totient = (self.p - 1) * (self.q - 1) // math.gcd(self.p - 1,
                                                               self.q - 1)  # totient(n), the number of coprimes with p and q from 1 to n is genterated
        self.numlist2 = []
        for icounter in range(2, self.totient):  # counts to one past upper limit (pre conditional)
            bprime = True  # predefines each number as prime, to be disproven
            ichecker = 2  # starts checker at 2, as that is the smallest prime
            while bprime != False and ichecker < int(
                    float(icounter ** (1 / 2) + 1)):  # allows exit when proven composite or after all test cases
                if icounter % ichecker == 0:  # checks if the mod of any number gives 0 indicating non prime
                    bprime = False  # sets prime value to false, so it is not counted in later commands
                else:
                    ichecker += 1  # ichecker moves onto next test number
            if bprime == True and self.totient % icounter != 0:
                self.numlist2.append(icounter)  # appends number
        self.e = self.numlist2[random.randint(0, len(self.numlist2))]

        self.d = RSA.MMI(self.e, self.totient)  # implementation of lambda
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #sets higher level variable to be used between methods

        self.encryptkey = (self.e, self.n)  # generates tuple to act as lock
        self.decryptkey = (self.d, self.n)  # generates tuple to act as key

    @staticmethod
    def encrypt(k1, k2, message):
        '''
        :param k1: exponential part of key
        :param k2: modulus part of key
        :param message: message to encrypt
        :return: string of numbers seperated by
        '''
        encrypted = []
        for letter in message:
            encrypted.append((ord(letter)) ** k1 % k2)
        return str(' '.join(str(n) for n in encrypted))

    def decrypt(self, emessage):  # takes an encrypted message
        '''
        :param emessage: This is an encrypted message, encrypted by the respective method in this very class or the staticmethod 'send'
        :return: The decrypted emessage as a string using the keys for the instance of conversation
        '''
        emessage = emessage.split(' ')
        decrypted = []  # creates an empty list
        for n in (emessage):
            decrypted.append((int(n) ** (self.decryptkey[0])) % (self.decryptkey[1]))  # Decrypts ASCII value (decrypted) to list
        decrypted = "".join(str(chr(n)) for n in decrypted)  # creates string from list of decrypted values and turns each ASCII to a character
        return decrypted

    def communicate(self, connector = False, OtherIP = '0.0.0.0', port = 34567):
        '''
        :param connector: Tells whether this computer will connect or bnd to server
        :param OtherIP: IP for connection to use, in case of connecting
        :param port: sets port for socket communication
        This program communicates the encryption key between computers and establishes a connection
        it then calls sends and recieve methods in parallel threads
        :return: none
        '''
        if connector:
            self.sock.connect((OtherIP, port))  #connects to specified ip, port
            keys = self.sock.recv(4096).decode(encoding='utf-8').split(' ') #recieves a message of the key parsed by a space
            k_1, k_2 = int(keys[0]), int(keys[1]) #turns the key to an int
            time.sleep(1)
            self.sock.send(((str(self.encryptkey[0])+" "+str(self.encryptkey[1]))).encode(encoding='utf-8')) #sends this objects key to other object

        else:
            self.sock.bind(('0.0.0.0', port))   #binds socket to port if not connecting
            self.sock.listen()
            self.sock = self.sock.accept()[0] #updates socket to connection
            self.sock.send((str(self.encryptkey[0])+" "+str(self.encryptkey[1]))).encode(encoding='utf-8') #sends key parsed by space
            time.sleep(1)
            keys = self.sock.recv(4096).decode(encoding='utf-8').split(' ') #Recieves key and parses it based on space
            k_1, k_2 = int(keys[0]), int(keys[1]) #wsets key values to int
            print('connected')

        a = threading.Thread(target= self.sends, args= (k_1, k_2)) # begins a parallel thread to send messages
        b = threading.Thread(target= self.receive) # begins a parallel thread to recieve messages
        a.start()
        b.start()

    def sends(self, k1, k2):
        '''
        This method sends messages encrypted
        :param k1: the exponent of the other key
        :param k2: the modulus of the other key
        :return: none
        '''
        while True:
            data = input("")
            self.sock.send(self.encrypt(k1, k2, data).encode(encoding='utf-8'))

    def receive(self):
        '''
        This method recieves all messages incoming and prints them decrypted
        :return: none
        '''
        while True:
            msg = self.sock.recv(4096).decode(encoding='utf-8')
            print(self.decrypt(msg))





p = RSA()
p.communicate(True, '192.168.0.19')
