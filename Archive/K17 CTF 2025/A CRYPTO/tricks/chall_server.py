#!/usr/bin/env python3
from Crypto.Util.number import getStrongPrime, long_to_bytes, bytes_to_long
from random import randint
import socket

FLAG = b"K17{g0oofY_LLL_p@1ll1Er_pRo6l3m}"
assert len(FLAG) == 32

class Paillier:
    def __init__(self, p, q):
        self.n = p * q
        self.n2 = self.n * self.n
        self.l = (p - 1) * (q - 1)
        self.mu = pow(self.l, -1, self.n)
        self.g = self.n + 1
        self.L = lambda x: (x - 1) // self.n

    def encrypt(self, m):
        return (pow(randint(1, self.n - 1), self.n, self.n2) * pow(self.g, m, self.n2)) % self.n2

    def decrypt(self, c):
        return (self.L(pow(c, self.l, self.n2)) * self.mu) % self.n

# generate keys once
p = getStrongPrime(1024)
q = getStrongPrime(1024)
paillier = Paillier(p, q)
ct_flag = paillier.encrypt(bytes_to_long(FLAG))

tricks = {
    "cha cha left": lambda x: x + b"\x00",
    "wave your hands": lambda x: b"\\_/-\\_/" + x + b"\\_/-\\_/",
    "SAY IT THREE TIMES": lambda x: x + x + x
}

HOST = "8.0.8.0"
PORT = 12345

def handle_conn(conn):
    def send(s):
        conn.sendall((s + "\n").encode())
    send("Welcome to Paillier tricks")
    send(f"paillier.n = {paillier.n}")
    send(f"ciphertext_of_flag = {ct_flag}")
    send("tricks: " + ", ".join(tricks.keys()))
    send("----")
    try:
        while True:
            send("Which trick do you want to show me? ")
            trick = conn.recv(4096).decode(errors="ignore").strip()
            if not trick:
                break
            if trick not in tricks:
                send("I've never heard of that trick before")
                continue
            send("What's the encrypted message you'd like to perform the trick on? ")
            x_line = conn.recv(4096).decode(errors="ignore").strip()
            send("What's the encrypted result of the trick? ")
            y_line = conn.recv(4096).decode(errors="ignore").strip()
            try:
                x = int(x_line); y = int(y_line)
            except:
                send("Invalid integer input.")
                continue
            try:
                dec_x = paillier.decrypt(x)
                dec_y = paillier.decrypt(y)
            except:
                send("Decryption error.")
                continue
            tx = long_to_bytes(dec_x)
            transformed = tricks[trick](tx)
            if bytes_to_long(transformed) == dec_y:
                send("HOLY SMOKES WHAT A TRICK!!!!!")
            else:
                send("nup.")
    finally:
        conn.close()

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((HOST, PORT))
    s.listen(1)
    print(f"Listening on {HOST}:{PORT}")
    while True:
        conn, addr = s.accept()
        print("Connection from", addr)
        handle_conn(conn)
