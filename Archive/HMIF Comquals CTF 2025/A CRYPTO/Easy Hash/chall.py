#!/usr/bin/env python3

from hashlib import sha256
import base64
import os
from libnum import s2n
from secret import FLAG

assert len(FLAG) == 78

KEY = os.urandom(32)

def get_hmac(data: bytes) -> str:
    return sha256(KEY + data).hexdigest()


def parse_token(token: str) -> dict:
    token_data, token_hmac = base64.b64decode(token).split(b":::hmac=")
    if get_hmac(token_data) != token_hmac.decode('latin-1'):
        return None

    user_data = dict()
    for part in token_data.decode('latin-1').split(":::"):
        key, value = part.split("=")
        user_data[key] = value

    return user_data


def register_user():
    name = input("Who are you?\n>>> ")

    user_data = {"user_id": 0, "name": name, "authorized": "false"}

    token = ":::".join(f"{key}={value}" for key, value in user_data.items())
    secure_token = f"{token}:::hmac={get_hmac(token.encode())}"
    encoded_secure_token = base64.b64encode(secure_token.encode()).decode('latin-1')

    print(f"Your access token: {encoded_secure_token}\n")


def login_user():
    user_data = parse_token(input("Enter access token: "))

    if user_data is None:
        print("Unverified login detected :(\n")
        return

    print(f"Hello {user_data['name']}, why don't you stay and relax here? [https://youtu.be/vy63u2hKoPE?si=CI0Fl5xu4sVj2DbK]\n")


def request_secret():
    user_data = parse_token(input("Enter access token: "))
    
    if user_data is None:
        print("Unverified login detected\n")
        return

    if user_data["authorized"] == "true":
        print("Hmmm looks forged to me...")
        user_id = int(user_data["user_id"], 2)
        enc1 = s2n(sha256(FLAG[user_id : user_id + 3].encode()).digest())
        enc2 = s2n(sha256(FLAG[user_id + 3 : user_id + 6].encode()).digest())
        enc3 = s2n(sha256(FLAG[user_id + 6 : user_id + 9].encode()).digest())
        print(f"I'm not gonna give the secret right away...\n{enc1 * enc2 * enc3}\n")
    else:
        print("Uh oh :-(\n")


def main():
    while True:
        print("1. Register\n2. Login \n3. Request Secret ;)\n4. Exit")

        try:
            choice = int(input("Enter your choice: "))
            if choice == 1:
                register_user()
            elif choice == 2:
                login_user()
            elif choice == 3:
                request_secret()
            elif choice == 4:
                break
            else:
                print("Invalid choice\n")
        except Exception:
            print(f"Oh no...\n")


if __name__ == "__main__":
    main()