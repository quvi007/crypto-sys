import socket
from diffie_hellmann import *
from aes import *

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = '127.0.0.1'
port = 50527
MODE = 128

s.bind((host, port))
s.listen(1)
conn, addr = s.accept()

# Secured Channel Handshake
data = conn.recv(1024).decode()
arr = data.split(" ")
p = int(arr[0])
g = int(arr[1])
g_a = int(arr[2])

b = generatePrime(MODE >> 1)
g_b = bigMod(g, b, p)

conn.sendall(str(g_b).encode())

keyInt = bigMod(g_a, b, p)
byte_array = keyInt.to_bytes((keyInt.bit_length() + 7) >> 3, byteorder='big')
byte_list = list(byte_array)
char_list = [chr(x) for x in byte_list]
keyText = ''.join(char_list)

aesInit(keyText, MODE)

# Handshake Done

print("Connected to", addr[0])

while True:
    data = conn.recv(1024).decode()
    
    decipheredTxt = AESDecryptText(data)
    print("Alice:", decipheredTxt)

    message = input("You: ")
    cipherTxt = AESEncryptText(message)
    conn.sendall(cipherTxt.encode())
