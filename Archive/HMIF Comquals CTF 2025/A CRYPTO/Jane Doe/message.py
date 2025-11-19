#!/usr/bin/env python3
import random
from Crypto.Util.number import getPrime
from reze import letter

BITS = 512

class LCG:
    def __init__(self, bits: int):
        self.bits = bits
        self.p = getPrime(bits + 1)
        self.b = random.getrandbits(bits)
        self.seed = random.getrandbits(bits)
        self.m = random.getrandbits(bits)

    def next(self) -> int:
        self.seed = (self.m * self.seed + self.b) % self.p
        self.m = random.getrandbits(self.bits)
        return self.seed

def split(data: bytes):
    if len(data) % 8 != 0:
        raise ValueError("FLAG length must be a multiple of 8 bytes.")
    out = []
    i = 0
    while i < len(data):
        block = data[i:i+8]
        val = int.from_bytes(block, "big")
        out.append(val)
        i += 8
    return out

def main():
    lcg = LCG(BITS)

    chunks = split(letter)
    enc = []
    idx = 0
    while idx < len(chunks):
        s = lcg.next()
        enc_val = s ^ chunks[idx]
        enc.append(enc_val)
        idx += 1

    hint = []
    j = 0
    while j < 64:
        s = lcg.next()
        hint.append(s)
        j += 1

    with open("output.txt", "w", encoding="utf-8") as f:
        f.write(f"b = {lcg.b}\n")
        f.write(f"p = {lcg.p}\n")
        f.write(f"enc = {enc}\n")
        f.write(f"hint = {hint}\n")

if __name__ == "__main__":
    main()
