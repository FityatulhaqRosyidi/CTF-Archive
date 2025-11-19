from Crypto.Util.number import *
import ecdsa, hashlib, signal

flag = open("flag.txt", "rb").read().strip()

E = ecdsa.curves.NIST384p
g = E.generator
n = E.order
p = E.curve.p()

def _dig(x: int, m: bytes):
    s = hashlib.sha512(str(x).encode() + m).digest()
    _ = hashlib.sha256(s).digest()
    return int.from_bytes(s, 'big') % n

def _round_down_pow2(z: int, b: int):
    q = 1 << b
    z -= (z % q)
    z &= -q
    return z or q

def _emsg(r, m: bytes):
    return int(hashlib.sha256(str(r).encode() + m).hexdigest(), 16) % n

def sign(x, m: bytes):
    k0 = _dig(x, m)
    k = _round_down_pow2(k0, ((1 << 4) - 2))
    R = g * k
    r = R.x() % n
    e = _emsg(r, m)
    s = (pow(k, -1, n) * (e + x * r)) % n
    return r, s

def verify(y, m: bytes, r, s):
    if not (1 <= r < n and 1 <= s < n):
        return False
    e = _emsg(r, m)
    w = pow(s, -1, n)
    u1 = (e * w) % n
    u2 = (r * w) % n
    P = g * u1 + y * u2
    v = P.x() % n
    return v == r

def print_banner():
    print("normal challenge i think")
    print("1. public key")
    print("2. sign")
    print("3. verify")
    print("4. flag")
    print("5. exit :(")

def challenge():
    private_key = getRandomRange(1, n - 1)
    public_key = g * private_key

    pt = '空に溶かせば　きらめく七色のRAINBOW, 見つめて　Believe in me, my mind'

    for _ in range(40):
        print_banner()
        try:
            choice = int(input(">> ").strip())
            
            if choice == 1:
                print(f"({public_key.x()}, {public_key.y()})")
                
            elif choice == 2:
                msg_hex = input("message in hex: ").strip()
                try:
                    message = bytes.fromhex(msg_hex)
                    
                    if message == pt.encode():
                        print("bbbbruhbruhbruh")
                        continue
                        
                    r, s = sign(private_key, message)
                    print(f"({r}, {s})")
                except ValueError:
                    print("bro whar")
                    
            elif choice == 3:
                msg_hex = input("message in hex: ").strip()
                r = int(input("input r: ").strip())
                s = int(input("input s: ").strip())
                
                try:
                    message = bytes.fromhex(msg_hex)
                    is_valid = verify(public_key, message, r, s)
                    print("validation:", "valid" if is_valid else "invalid")
                except ValueError:
                    print("bro whar")
                    
            elif choice == 4:
                r = int(input("input r: ").strip())
                s = int(input("input s: ").strip())
                
                if verify(public_key, pt.encode(), r, s):
                    print("fire emoji here flag")
                    print(flag.decode())
                    exit(0)
                else:
                    print("invalid >:(")
                    
            elif choice == 5:
                print("bye~")
                exit(0)
                
            else:
                print("?")
                
        except Exception as e:
            print(f"error: {e}")
    
    print("expired :(")

if __name__ == "__main__":
    try:
        signal.alarm(200)
        challenge()
    except Exception as e:
        print(f"exception: {e}")
        exit(1)