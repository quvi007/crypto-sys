import socket
from diffie_hellmann import *
from aes import *

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = '127.0.0.1'
port = 50527
MODE = 128

s.connect((host, port))

# Secured Channel Handshake
p = generateSafePrime(MODE)
g = primitiveRoot(p, 2, p - 1)
a = generatePrime(MODE >> 1)
g_a = bigMod(g, a, p)

s.sendall((str(p) + " " + str(g) + " " + str(g_a)).encode())

data = s.recv(1024).decode()
g_b = int(data)

keyInt = bigMod(g_b, a, p)
byte_array = keyInt.to_bytes((keyInt.bit_length() + 7) >> 3, byteorder='big')
byte_list = list(byte_array)
char_list = [chr(x) for x in byte_list]
keyText = ''.join(char_list)

aesInit(keyText, MODE)

# Handshake Done

while True:
    message = input("You: ")
    cipherTxt = AESEncryptText(message)
    s.sendall(cipherTxt.encode())

    data = s.recv(1024).decode()
    decipheredTxt = AESDecryptText(data)
    print("Bob:", decipheredTxt)
