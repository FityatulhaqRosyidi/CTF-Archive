import secrets
import sympy
from typing import Tuple

FLAG = "CTFITB2025{?????????????????????????????????????????????????}"
BITS = 512
LIM = 1 << BITS

def diff(x: int) -> int:
    return sum(int(y) for y in bin(x)[2:])

def gen(bits: int) -> int:
    half = LIM // 2
    while True:
        cand = secrets.randbelow(half) + half
        if sympy.isprime(cand) and (cand - 1) % 3 != 0:
            return cand

def keygen(bits: int = BITS) -> Tuple[int, int, int]:
    e = 3
    while True:
        p = gen(bits)
        q = gen(bits)
        n = p * q
        if n > (1 << 1023):
            break
    phi = (p - 1) * (q - 1)
    d = pow(e, -1, phi)
    secret = secrets.randbelow(LIM)
    sig = pow(secret, d, n)
    return n, secret, sig

def truth(n: int, secret: int) -> None:
    while True:
        print("And I just realized")
        msg = input()
        if msg == "guess":
            print("Doesn't anyone want my heart?")
            try:
                guess_val = int(input())
            except ValueError:
                print("I'm sorry, Denji kun...")
                exit(0)
            if guess_val == secret:
                print("Honestly, I really do like you:")
                print(FLAG)
                exit(0)
            else:
                print("I'm sorry, Denji kun...")
                exit(0)

        msg_int = int(msg)
        enc = pow(msg_int, 3, n)
        print(diff(enc) % 2)

def main() -> None:
    n, secret, sig = keygen(BITS)
    print("The truth is: " + str(sig))
    truth(n, secret)

if __name__ == "__main__":
    main()
