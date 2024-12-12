from aes import *
import time

def main():
    print("Enter the plain text:")
    txt = input()
    print("Enter key size in bits:")
    sz = int(input())
    print("Enter the key:")
    key = input()
    
    print("Plain Text:")
    print(f"In ASCII: {txt}")
    print("In HEX:", end = " ")
    printHex(txt)
    print()

    print(f"Key:")
    print(f"In ASCII: {key}")
    print("In HEX:", end = " ")
    printHex(key)
    print()

    start_time = time.time()
    aesInit(key, sz)
    end_time = time.time()
    keySchedTime = end_time - start_time

    start_time = time.time()
    cipherTxt = AESEncryptText(txt)
    end_time = time.time()
    enc_time = end_time - start_time
    print("Cipher Text:")
    print("In HEX:", end = " ")
    printHex(cipherTxt)
    print(f"In ASCII: {cipherTxt}")
    print()

    start_time = time.time()
    decipherTxt = AESDecryptText(cipherTxt)
    end_time = time.time()
    dec_time = end_time - start_time
    print("Deciphered Text:")
    print("In HEX:", end = " ")
    printHex(decipherTxt)
    print(f"In ASCII: {decipherTxt}")
    print()
    
    print("Execution time details:")
    print(f"Key Scheduling : {keySchedTime * 1000} ms")
    print(f"Encryption Time : {enc_time * 1000} ms")
    print(f"Decryption Time : {dec_time * 1000} ms")

main()