from sage.all import *
from Crypto.Cipher import AES
from Crypto.Util.number import *
from Crypto.Util.Padding import pad
from mpmath import mp
from os import urandom

import json
import random

FLAG = open("flag.txt", "rb").read().strip()

mp.dps = 1000

def lift_x(x):
    return mp.sqrt((x**2-1)/(2*x**2 - 1))

def double(pt):
    x, y = pt
    xf = (2*x*y)/(1 + 2*x**2*y**2)
    yf = (y**2 - x**2)/(1 - 2*x**2*y**2)
    return (xf, yf)

def add(pt1, pt2):
    x1, y1 = pt1
    x2, y2 = pt2
    xf = (x1*y2 + x2*y1)/(1+2*x1*x2*y1*y2)
    yf = (y1*y2 - x1*x2)/(1-2*x1*x2*y1*y2)
    return (xf, yf)

def scalar_multiply(pt, m):
    if m == 1:
        return pt
    half_mult = scalar_multiply(pt, m // 2)
    ans = double(half_mult)
    if m % 2 == 1:
        ans = add(ans, pt)
    return ans

key = urandom(16)
iv = urandom(16)
cipher = AES.new(key, AES.MODE_CBC, iv)
plaintext = pad(FLAG, 16)
ciphertext = cipher.encrypt(plaintext)

N = bytes_to_long(key)

gx = mp.mpf(random.random())
gy = lift_x(gx)
G = (gx, gy)
P = scalar_multiply(G, N)

json.dump({
    'gx': str(G[0]),
    'gy': str(G[1]),    
    'px': str(P[0]),
    'py': str(P[1]),
    'ciphertext': ciphertext.hex(),
    'iv': iv.hex(),
}, open('output.txt', 'w'))
