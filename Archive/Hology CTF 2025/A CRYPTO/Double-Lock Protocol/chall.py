
import os, sys, base64, random, hashlib, hmac
from Crypto.Util.number import getPrime, bytes_to_long, long_to_bytes
from Crypto.Random import get_random_bytes

BITS = 1024
PB = BITS // 2
E = 65537

def base64_safe(b): return base64.b64encode(b).decode()

def emit_pow_line(prefix, difficulty):
    sys.stdout.write(f"POW {prefix} {difficulty}\n"); sys.stdout.flush()

def check_pow(prefix, difficulty, nonce):
    h = hashlib.sha256((prefix + nonce).encode()).hexdigest()
    return h.startswith("0" * difficulty)

def rsa_ct_bytes(n, m_bytes):
    m_int = bytes_to_long(m_bytes)
    if m_int >= n:
        raise SystemExit(1)
    c = pow(m_int, E, n)
    blen = (c.bit_length() + 7) // 8
    return c.to_bytes(blen, 'big')

def main():

    fp = os.path.join(os.path.dirname(__file__), "flag.txt")
    if not os.path.isfile(fp):
        sys.exit("flag.txt missing")
    FLAG = open(fp,'rb').read().strip()

    prefix1 = base64_safe(get_random_bytes(6))[:8]
    diff1 = 6
    emit_pow_line(prefix1, diff1)
    line = sys.stdin.readline()
    if not line:
        return
    if not check_pow(prefix1, diff1, line.strip()):
        sys.stdout.write("ERR\n"); sys.stdout.flush(); return

    sys.stdout.flush()

if __name__ == "__main__":
    main()

