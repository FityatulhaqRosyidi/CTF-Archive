from Crypto.Cipher import Salsa20
from Crypto.Util.number import bytes_to_long, long_to_bytes
import random as rng
import ast
from secrets import token_bytes
from zlib import crc32
import hashlib
import os


FLAG = b"SCH25{yyyyyyytttttttttttttttttttttttttttaaaaaaaaaaa}"
KEY = token_bytes(32)


def verification(key,data):
        return hashlib.sha1(key[:16] + data).hexdigest()


def encrypt_ticket(team_name, OTP):
    cipher = Salsa20.new(key=KEY)
    nonce = cipher.nonce
    data={}
    team_id = hex(crc32(team_name.encode()))[2:]
    data['ticket'] = (team_name+'-'+team_id).encode()
    checksum = verification(KEY,data['ticket'])
    data = str(data).encode()
    ciphertext = cipher.encrypt(data)
    print('Your encrypted ticket is:', (nonce + bytes.fromhex(checksum) + ciphertext).hex())
    print('Team OTP: ', OTP,'\n')


def read_ticket(ticket,OTP):
    packet = bytes.fromhex(ticket)
    nonce = packet[:8]
    checksum = packet[8:28].hex()
    ciphertext = packet[28:]
    try:
        cipher = Salsa20.new(key=KEY, nonce=nonce)
        plaintext = str(cipher.decrypt(ciphertext))[2:-1]
        plaintext = ast.literal_eval(plaintext)

        if verification(KEY[:16],plaintext['ticket']) != checksum:
            print('Invalid checksum. Aborting!')
            return

        parsed = plaintext['ticket'].split(b'-')        
        if len(parsed) == 3 and parsed[-1] == OTP.encode():
             print(parsed[0].decode(),'team ready to play!!')
             print(FLAG.decode())
        else:
              print('Expired!')
              return 0

    except:
        print('Invalid data. Aborting!')


def menu():
    print('[G]et ticket')
    print('[I]nsert ticket')
    print('[Q]uit')

    
def main():
    print('Ready?, Get your ticket here!!\n')    
    OTP = hex(rng.getrandbits(32))[2:]
    while True:        
        menu()
        option = input('\n>> ').upper()
        
        if option == 'G':
            team_name = input('Your team name: ')
            if len(team_name) > 5:
                print('Team name too long!!\n')
                continue
            encrypt_ticket(team_name,OTP)
            OTP = hex(rng.getrandbits(32))[2:]

        elif option == 'I':            
            ticket = input('Your encrypted ticket (hex): ')
            if(read_ticket(ticket,OTP) == 0):
                exit(0)

        elif option == 'Q':
            exit(0)

        else:
            print('Invalid option!!\n')


if __name__ == '__main__':
    main()