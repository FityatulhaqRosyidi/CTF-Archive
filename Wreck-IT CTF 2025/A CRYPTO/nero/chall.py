from Crypto.Util.number import isPrime
import random

FLAG = open('flag.txt').read()
p = int(input("Choose p > "))
if not isPrime(p) or p.bit_length() < 1000:
    print("Fail")
    exit(1)

x = random.randint(3, p-1)

def f(x):
    res = 0
    for i in range(7):
        if i==5: continue
        res += pow(i, x, p)
        res %= p
    return res

res = f(x)
print(res)

guess = int(input("guess? > "))
if guess == x:
    print(FLAG)