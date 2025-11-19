import secrets; import hashlib
from Crypto.Cipher import AES
from Crypto.Util.number import getPrime
from Crypto.Util.Padding import pad

N_SIZE   = 1024
SAMPLES  = 30
R_BITLEN = 100

def gen(N_size: int, samples: int, r_bits: int):
    N = secrets.randbits(N_size) | (1 << N_size)
    d = N
    while d >= N:
        d = getPrime(N_size)

    R = []
    values = []
    for _ in range(samples):
        r = secrets.randbits(r_bits)
        alpha = N + r
        R.append(r)
        values.append(pow(d, -1, alpha))

    return N, d, R, values


with open("story.txt", "rb") as f:
    flag = f.read()

N, d, R, values = gen(N_SIZE, SAMPLES, R_BITLEN)

key  = hashlib.sha256(str(d).encode()).digest()
flag = pad(flag, 16)
c = AES.new(key, AES.MODE_CBC)
iv  = c.iv.hex()
enc = c.encrypt(flag).hex()

with open("out.txt", "w", encoding="utf-8") as f:
    f.write(f"{R = }\n")
    f.write(f"{values = }\n")
    f.write(f"{'iv'} = '{iv}'\n")
    f.write(f"{'enc'} = '{enc}'\n")
