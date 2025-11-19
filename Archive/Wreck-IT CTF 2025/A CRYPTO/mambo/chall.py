from Crypto.Util.number import getPrime
from libnum import s2n
import secrets

flag = open("flag.txt", "rb").read()
flag = s2n(flag)
p = getPrime(512)
q = getPrime(512)
N = p * q
e = 5
k = 8

cs = [secrets.randbelow(N) for _ in range(k)]
sum_cs = sum(cs) % N

cts = []
for c in cs:
    flag ^= c
    cts.append(pow(c, e, N))

with open('output.txt', 'w+') as f:
    f.write(f'{N=}\n')
    f.write(f'{sum_cs=}\n')
    f.write(f'{cts=}\n')
    f.write(f'{flag=}\n')