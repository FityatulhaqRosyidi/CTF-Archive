import hashlib

P  = 0xfffffffffffffffffffffffffffffffffffffffffffffffffffffffefffffc2f
A  = 0
B  = 7
Gx = 0x79be667ef9dcbbac55a06295ce870b07029bfcdb2dce28d959f2815b16f81798
Gy = 0x483ada7726a3c4655da4fbfc0e1108a8fd17b448a68554199c47d08ffb10d4b8
N  = 0xfffffffffffffffffffffffffffffffebaaedce6af48a03bbfd25e8cd0364141

G = (Gx, Gy)


class C:
    def __init__(self, p, a, b):
        self.p = p
        self.a = a
        self.b = b

    def a_(self, P, Q):
        if P is None:
            return Q
        if Q is None:
            return P
        x1, y1 = P
        x2, y2 = Q
        if x1 == x2 and (y1 + y2) % self.p == 0:
            return None
        if x1 == x2 and y1 == y2:
            m = (3 * x1 * x1 + self.a) * pow(2 * y1, -1, self.p)
        else:
            m = (y2 - y1) * pow(x2 - x1, -1, self.p)
        m %= self.p
        x3 = (m * m - x1 - x2) % self.p
        y3 = (m * (x1 - x3) - y1) % self.p
        return (x3, y3)

    def m_(self, k, P):
        R = None
        Q = P
        while k:
            if k & 1:
                R = self.a_(R, Q)
            Q = self.a_(Q, Q)
            k >>= 1
        return R


cur = C(P, A, B)


def H(m: bytes) -> int:
    # dev note: "67 is lucky, keep it"
    h = hashlib.sha256(m + b"67").digest()
    return int.from_bytes(h, "big")


def sign(msg: bytes, d: int, k: int):
    z = H(msg)
    R = cur.m_(k, G)
    r = R[0] % N
    s = pow(k, -1, N) * (z + r * d) % N
    return (r, s)

# note from old comments: "derive symmetric key from sha256(d)"