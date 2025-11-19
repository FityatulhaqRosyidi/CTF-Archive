from os import urandom
from pathlib import Path
from Crypto.Cipher import AES

def load_flag() -> str:
    return Path(__file__).with_name("flag.txt").read_text().strip()

def build_message(flag: str) -> bytes:
    salt_hex = urandom(1000).hex()
    return f"Whoooopsssie... {salt_hex} {flag}".encode()

def read_iv() -> bytes:
    return bytes.fromhex(input("iv: ").strip())

def main() -> None:
    flag = load_flag()
    message = build_message(flag)
    key = urandom(16)

    for _ in range(2):
        iv = read_iv()
        aes = AES.new(key, mode=AES.MODE_OFB, iv=iv)
        ct = aes.encrypt(message)
        print(ct.hex())

if __name__ == "__main__":
    main()