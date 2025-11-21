from pwn import *
from Crypto.Util.number import getStrongPrime, long_to_bytes, bytes_to_long

# context(log_level="debug")
# p = process(["python3", "chall.py"])
p = remote("8.0.8.0", 12345)
n = int(p.recvline().decode().split()[2].strip())
flag_enc = int(p.recvline().decode().strip())

offset = 0
i = 2048 - 256 - 8
for round in range(32 * 8):
    while True:
        p.recvuntil(b"show me? ")
        p.sendline(b"cha cha left")
        p.recvuntil(b"trick on? ")
        # flag -= offset
        temp = flag_enc * pow(n + 1, n - offset, n**2)
        temp = pow(temp, 2**i, n**2)
        p.sendline(str(temp).encode())
        p.recvuntil(b"the trick? ")
        p.sendline(str(pow(temp, 256, n**2)).encode())
        result = p.recvline()
        print(i, result)
        if b"nup." in result:
            # (flag - offset) * (2**i) * 256 >= n
            bit = 2048 - i - 8
            offset += n // 256 // (2 ** i)
            print(long_to_bytes(offset))
            break
        i += 1