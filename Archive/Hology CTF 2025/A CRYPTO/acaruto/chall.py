from Crypto.Util.number import *


# FLAG = open('flag.txt').read()
FLAG = "ASDS"
ACARUTO = 'Hey it\'s me Acaruto! I am the pillar of life. You don\'t know me, but I know everyone'.encode()


def encrypt(e, n):
    try:
        msg = input('Enter the message: ')
        assert msg.isascii()
    except AssertionError:
        print('Invalid input!')
    else:
        if msg.encode() == ACARUTO:
            print('Not allowed!')
            return

        enc = pow(bytes_to_long(msg.encode()), e, n)
        print('Encrypted message in hex:', hex(enc)[2:])


def check(d, n):
    try:
        enc = int(input('Enter the message in hex: '), 16)
    except ValueError:
        print('Invalid input!')
    else:
        if enc > n:
            print('Not allowed!')
            return

        msg = pow(enc, d, n)
        if long_to_bytes(msg) == ACARUTO:
            print('You got it! Here\'s the flag:', FLAG)
        else:
            print('Not yet :(')


def main():
    while True:
        try:
            p = getPrime(1024)
            q = getPrime(1024)
            n = p * q
            e = 0x10001
            d = pow(e, -1, (p-1)*(q-1))
        except:
            continue
        else:
            break

    while True:
        try:
            choice = int(input('Select one:\n1) Encrypt\n2) Check\n>> '))
            assert 1 <= choice <= 2
        except:
            print('Invalid choice!')
            break
        else:
            if choice == 1:
                encrypt(e, n)
            elif choice == 2:
                check(d, n)


if __name__ == '__main__':
    main()
