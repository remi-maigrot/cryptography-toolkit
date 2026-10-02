# Cryptography Toolkit

A command-line encryption tool in Python implementing XOR, a simplified symmetric cipher and RSA from scratch — no third-party crypto libraries.

## About

Epitech project (2023). The goal was to build `mypgp`, a small PGP-inspired program that encrypts and decrypts messages with both symmetric and asymmetric algorithms, implementing the underlying math by hand (modular arithmetic, primality testing, key generation) instead of relying on existing cryptography packages.

> This is an educational implementation. It is not meant to protect real data.

## Features

- **XOR cipher** — encrypts / decrypts hex-encoded messages with a hex key (`-xor`).
- **Simplified symmetric cipher** (`-aes` flag) — byte-wise XOR of a UTF-8 message with a text key, output as hex. It is *not* a real AES implementation.
- **RSA**
  - Key-pair generation (`-g`): random primes validated with the **Miller–Rabin** primality test (128 rounds), public exponent `e = 65537`, private exponent computed with the **extended Euclidean algorithm** (modular inverse).
  - Keys printed as little-endian hexadecimal in `exponent-modulus` form.
  - Encryption and decryption with fast modular exponentiation.
- Message read from standard input, so the tool composes with shell pipes.

## Tech stack

- Python 3 (standard library only: `random`, `math`, `sys`)
- GNU Make

## Architecture

```
src/
├── main.py           Entry point: parse arguments, dispatch to the selected algorithm
├── manage_algos.py   CLI parsing + XOR and simplified symmetric cipher
└── RSA.py            RSACryptosystem: Miller–Rabin, xgcd / modinv, key generation,
                      encrypt / decrypt, little-endian hex conversion
```

## Build & Run

Requirements: Python 3 and `make`.

```bash
make            # produces the ./mypgp executable
make re         # rebuild
make fclean     # remove the executable
```

`mypgp` imports the `src` package, so run it from the repository root.

```bash
./mypgp -h

# XOR: message and key are hex strings
echo -n "48656c6c6f" | ./mypgp -xor -c 0102030405     # -> 49676f686a
echo -n "49676f686a" | ./mypgp -xor -d 0102030405     # -> 48656c6c6f

# RSA: generate a key pair
./mypgp -rsa -g d3 e3

# RSA: encrypt with the public key, decrypt with the private key
echo -n "Hello" | ./mypgp -rsa -c <public-key>
echo -n "<ciphertext>" | ./mypgp -rsa -d <private-key>
```

Usage summary:

```
./mypgp [-xor | -aes | -rsa] [-c | -d] [-b] KEY
    -c      cipher the message read from stdin
    -d      decipher the message read from stdin
    -b      block mode (message and key of the same size)
    -g P Q  RSA only: generate a public / private key pair
```
