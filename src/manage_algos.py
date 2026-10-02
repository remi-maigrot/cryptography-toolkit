#!/usr/bin/env python3

##
## EPITECH PROJECT, 2023
## B-CNA-500-BDX-5-1-cryptography-remi.maigrot
## File description:
## pgp
##

import sys
from math import *
from random import *
from src.RSA import RSACryptosystem

class ManageAlgos:
    def __init__(self):
        self.key = None
        self.message = "Je suis un message!"
        self.algorithm = None
        self.mode = None
        self.block = None
        self.p = None
        self.q = None

    def manage_parsing(self) -> None:
        if len(sys.argv) < 2 or sys.argv[1] == "-h":
            self.help()
            sys.exit(1)

        algorithms = ['-xor', '-aes', '-rsa', '-pgp']
        modes = ['-c', '-d']
        block_mode = '-b'
        key_generation = '-g'

        for arg in sys.argv[1:]:
            if arg in algorithms:
                self.algorithm = arg[1:]
            elif arg in modes:
                self.mode = arg[1:]
            elif arg == block_mode:
                self.block = True
            elif arg == key_generation and self.algorithm == 'rsa':
                try:
                    self.p = sys.argv[sys.argv.index(arg) + 1]
                    self.q = sys.argv[sys.argv.index(arg) + 2]
                except (IndexError, ValueError):
                    print("Invalid P and Q values for RSA key generation")
                    sys.exit(1)
            else:
                self.key = arg

        if not self.algorithm or (not self.mode and not self.p and not self.q):
            print("Missing algorithm or mode")
            self.help()
            sys.exit(1)

    def help(self) -> None:
        print("USAGE", end='\n')
        print("    ./mypgp [-xor | -aes | -rsa] [-c | -d] [-b] KEY", end='\n\n')
        print("    the MESSAGE is read from standard input", end='\n')
        print("DESCRIPTION", end='\n')
        print("    -xor    computation using XOR algorithm", end='\n')
        print("    -aes    computation using AES algorithm", end='\n')
        print("    -rsa    computation using RSA algorithm", end='\n')
        print("    -c      MESSAGE is clear and we want to cipher it", end='\n')
        print("    -d      MESSAGE is ciphered and we want to decipher it", end='\n')
        print("    -b      block mode: for xor and aes, only works on one block", end='\n')
        print("            MESSAGE and KEY must be of the same size", end='\n')
        print("    -g P Q  for RSA only: generate a public and private key", end='\n')
        print("            pair from the prime number P and Q", end='\n')

    def xor_encryption(self, message: str) -> str:
        message = message.replace('"', '').replace("'", '').strip()
        message_bytes = bytes.fromhex(message)
        key_bytes = bytes.fromhex(self.key)

        encrypted_bytes = bytes([mb ^ kb for mb, kb in zip(message_bytes, key_bytes)])

        return encrypted_bytes.hex()

    def xor_decryption(self, encrypted_message: str) -> str:
        # Nettoyer le message des guillemets et des espaces blancs
        encrypted_message = encrypted_message.replace('"', '').replace("'", '').strip()
        
        # Convertir le message chiffré et la clé en octets
        encrypted_message_bytes = bytes.fromhex(encrypted_message)
        key_bytes = bytes.fromhex(self.key)

        # Déchiffrement XOR
        decrypted_bytes = bytes([emb ^ kb for emb, kb in zip(encrypted_message_bytes, key_bytes)])

        # Convertir le résultat en hexadécimal pour l'affichage
        return decrypted_bytes.hex()

    def aes_encryption(self, message: str) -> str:
        # Ici, nous utilisons une version très simplifiée pour le chiffrement AES
        # Cette implémentation n'est pas sécurisée et est à but éducatif seulement
        message_bytes = bytes(message, 'utf-8')
        key_bytes = bytes(self.key, 'utf-8')
        encrypted_bytes = bytes([mb ^ kb for mb, kb in zip(message_bytes, key_bytes)])
        return encrypted_bytes.hex()
    
    def aes_decryption(self, encrypted_message: str) -> str:
        # La procédure de déchiffrement est une inversion du chiffrement
        encrypted_message_bytes = bytes.fromhex(encrypted_message)
        key_bytes = bytes(self.key, 'utf-8')
        decrypted_bytes = bytes([emb ^ kb for emb, kb in zip(encrypted_message_bytes, key_bytes)])
        return decrypted_bytes.decode('utf-8', errors='ignore')

    def launch(self) -> None:
        if len(sys.argv) < 2:
            print("No input provided")
            self.help()
            sys.exit(1)

        # Lire le message depuis argv
        if (not self.p and not self.q):
            self.message = sys.stdin.read().strip()

        if self.algorithm == "xor":
            if self.mode == "c":
                # Chiffrement XOR
                encrypted_message = self.xor_encryption(self.message)
                print(encrypted_message)
            elif self.mode == "d":
                # Déchiffrement XOR
                decrypted_message = self.xor_decryption(self.message)
                print(decrypted_message)
            else:
                print("Invalid mode for XOR")
        elif self.algorithm == "aes":
            if self.mode == "c":
                # Chiffrement AES
                encrypted_message = self.aes_encryption(self.message)
                print(encrypted_message)
            elif self.mode == "d":
                # Déchiffrement AES
                decrypted_message = self.aes_decryption(self.message)
                print(decrypted_message)
            else:
                print("Invalid mode for AES")
        elif self.algorithm == "rsa":
            rsa = RSACryptosystem()
            if '-g' in sys.argv:
                # Génération de clés RSA
                self.p = int(self.p, 16)
                self.q = int(self.q, 16)
                p = rsa.generate_prime(self.p)
                q = rsa.generate_prime(self.q)
                public_key, private_key = rsa.generate_keypair_from_primes(p, q)
                print("public key: ", public_key[1], '-', public_key[0], sep='')
                print("private key: ", private_key[1], '-', private_key[0], sep='')
            else:
                # Chiffrement ou Déchiffrement RSA
                key_parts = self.key.split('-')
                if len(key_parts) != 2:
                    print("Invalid RSA key format")
                    sys.exit(1)

                key_part1 = key_parts[1]
                key_part2 = key_parts[0]

                if self.mode == "c":
                    # Chiffrement RSA
                    encrypted_message = rsa.encrypt_rsa(self.message, key_part1, key_part2)
                    print(encrypted_message)
                elif self.mode == "d":
                    # Déchiffrement RSA
                    self.message = int(self.message)
                    decrypted_message = rsa.decrypt_rsa(self.message, key_part1, key_part2)
                    if (decrypted_message == None):
                        sys.exit(1)
                    print(decrypted_message)
                else:
                    print("Invalid mode for RSA")
        else:
            print("Unknown algorithm")
