import random

class RSACryptosystem:
    def __init__(self):
        pass

    def is_prime(self, n, k=128):
        if n == 2 or n == 3:
            return True
        if n <= 1 or n % 2 == 0:
            return False
        r, d = 0, n - 1
        while d % 2 == 0:
            r += 1
            d //= 2
        for _ in range(k):
            a = random.randint(2, n - 2)
            x = pow(a, d, n)
            if x == 1 or x == n - 1:
                continue
            for _ in range(r - 1):
                x = pow(x, 2, n)
                if x == n - 1:
                    break
            else:
                return False
        return True

    def generate_prime(self, bits):
        while True:
            num = random.getrandbits(bits)
            num |= 1
            if self.is_prime(num):
                return num

    def xgcd(self, a, b):
        x0, y0, x1, y1 = 1, 0, 0, 1
        while b != 0:
            q, a, b = a // b, b, a % b
            x0, x1 = x1, x0 - q * x1
            y0, y1 = y1, y0 - q * y1
        return a, x0, y0

    def modinv(self, a, m):
        g, x, _ = self.xgcd(a, m)
        if g != 1:
            raise Exception('Modular inverse does not exist')
        return x % m

    def convert_to_little_endian_hex(self, number):
        hex_str = hex(number)[2:]
        if len(hex_str) % 2 != 0:
            hex_str = '0' + hex_str
        return ''.join(reversed([hex_str[i:i+2] for i in range(0, len(hex_str), 2)]))

    def generate_keypair_from_primes(self, p, q):
        n = p * q
        phi = (p - 1) * (q - 1)
        e = 65537
        d = self.modinv(e, phi)
        n_le = self.convert_to_little_endian_hex(n)
        e_le = self.convert_to_little_endian_hex(e)
        d_le = self.convert_to_little_endian_hex(d)
        return ((n_le, e_le), (n_le, d_le))

    def encrypt_rsa(self, message, key_n, key_e):
        key_n_int = self.hex_to_int_little_endian(key_n)
        key_e_int = self.hex_to_int_little_endian(key_e)
        message_int = int.from_bytes(message.encode(), byteorder='big')
        encrypted_int = pow(message_int, key_e_int, key_n_int)
        return encrypted_int

    def decrypt_rsa(self, encrypted, key_n, key_d):
        try:
            key_n_int = self.hex_to_int_little_endian(key_n)
            key_d_int = self.hex_to_int_little_endian(key_d)

            decrypted_int = pow(encrypted, key_d_int, key_n_int)
            decrypted_message = decrypted_int.to_bytes((decrypted_int.bit_length() + 7) // 8, 'big').decode()
            return decrypted_message
        except Exception as e:
            print("Invalid private key to decrypt the message.")
            return None

    def hex_to_int_little_endian(self, hex_str):
        big_endian_hex = ''.join(reversed([hex_str[i:i+2] for i in range(0, len(hex_str), 2)]))
        return int(big_endian_hex, 16)


if __name__ == "__main__":
    rsa = RSACryptosystem()

    # Génération de nombres premiers pour les tests
    p_example = rsa.generate_prime(int('d3', 16))
    q_example = rsa.generate_prime(int('e3', 16))

    # Génération des clés publiques et privées
    public_key, private_key = rsa.generate_keypair_from_primes(p_example, q_example)

    print("Public key:", public_key)
    print("Private key:", private_key)

    # Chiffrement et déchiffrement du message
    message = "Hello RSA Encryption!"
    encrypted_message = rsa.encrypt_rsa(message, public_key[0], public_key[1])
    print(type(encrypted_message), type(private_key[0]), type(private_key[1]))
    print("encrypted_message", encrypted_message)
    decrypted_message = rsa.decrypt_rsa(encrypted_message, private_key[0], private_key[1])

    print("Encrypted message:", encrypted_message)
    print("Decrypted message:", decrypted_message)