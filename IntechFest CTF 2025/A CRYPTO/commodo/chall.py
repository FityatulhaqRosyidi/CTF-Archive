import os
import base64
from Crypto.PublicKey import RSA
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from Crypto.Util import number

flag_env = os.environ.get("CHALL_FLAG")
flag_bytes = flag_env.encode()

g = 5
e1_prime = 65537
e2_prime = 48611

key_params = RSA.generate(2048)
n = key_params.n
e1 = g * e1_prime
e2 = g * e2_prime

key_en = RSA.construct((n, e1))
key_si = RSA.construct((n, e2))

pem_en = key_en.export_key().decode()
pem_si = key_si.export_key().decode()

bits = 1024
p_pi = number.getPrime(bits)
q_pi = p_pi
while True:
    q_pi += 2
    if number.isPrime(q_pi) and q_pi.bit_length() == bits and q_pi != p_pi:
        break
n_pi = p_pi * q_pi
e_pi = 65537
key_pi = RSA.construct((n_pi, e_pi))
pem_pi = key_pi.export_key().decode()

decoy_message = b"Maybe there's something common between two other keys?"
m_decoy = int.from_bytes(decoy_message, "big")
c_decoy = pow(m_decoy, key_pi.e, key_pi.n)

aes_key = os.urandom(16)
cipher_aes = AES.new(aes_key, AES.MODE_CBC)
encrypted_flag = cipher_aes.encrypt(pad(flag_bytes, AES.block_size))
iv = cipher_aes.iv
iv_and_ct = iv + encrypted_flag

m = int.from_bytes(aes_key, "big")
c1 = pow(m, key_en.e, key_en.n)
c2 = pow(m, key_si.e, key_si.n)

parts = []
parts.append("=== publickey_en.pem ===")
parts.append(pem_en)
parts.append("\n=== publickey_si.pem ===")
parts.append(pem_si)
parts.append("\n=== publickey_pi.pem ===")
parts.append(pem_pi)

parts.append("\n=== key_for_en.enc ===")
parts.append(int_to_b64(c1))
parts.append("\n=== key_for_si.enc ===")
parts.append(int_to_b64(c2))
parts.append("\n=== key_for_pi.enc ===")
parts.append(int_to_b64(c_decoy))

parts.append("\n=== flag.enc ===")
parts.append(base64.b64encode(iv_and_ct).decode())

return "\n".join(parts).encode()