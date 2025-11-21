from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from hashlib import md5
import random
import os

KEY = os.urandom(16)
FLAG = open('flag.txt', 'rb').read()
K = 2

def encrypt(data: bytes, K: int = K):
    pt = pad(data, 16)
    iv = md5(pt).digest()[:16]
    ct = pt
    for _ in range(K):
        cipher = AES.new(KEY, AES.MODE_CBC, iv) 
        ct = cipher.encrypt(ct)
    return iv, ct

def decrypt(data: bytes, iv: bytes):
    pt = data
    for _ in range(K):
        cipher = AES.new(KEY, AES.MODE_CBC, iv) 
        pt = cipher.decrypt(pt)
    pt = unpad(pt, 16)
    return pt

def chall():
    global KEY
    IV, CT = encrypt(FLAG)
    while True:
        try:
            choice = int(input(">> "))
            if choice == 1:
                # Encrypt
                data = bytes.fromhex(input("Data (hex): "))
                iv, ct = encrypt(data)
                print(ct.hex())
            elif choice == 2:
                data = bytes.fromhex(input("Data (hex): "))
                iv = bytes.fromhex(input("IV (hex): "))
                pt = decrypt(data, iv)
                print(ct.hex())
            elif choice == 3:
                # Flag
                print(IV.hex())
                print(CT.hex())
            elif choice == 4:
                KEY = os.urandom(16)
                IV, CT = encrypt(FLAG)
                print("Done")
            else:
                print("Bye")
                exit(0)
        except Exception as e:
            print("Nope")
            
if __name__ == "__main__":
    chall()