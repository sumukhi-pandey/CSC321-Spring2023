# %%
from Crypto.Cipher import AES 
from Crypto.Random import get_random_bytes
from Crypto.Util import number
import hashlib
import random
import sys
python_version = sys.version_info
if (python_version.major == 3 and python_version.minor > 7):
    import time # PyCryptodome library uses time.clock as dependency, but
    time.clock = time.time # time.clock was depricated in Python 3.8

BIT_LENGTH = 2048
E = 65537

# %%
def get_rsa_keys():
    p = number.getPrime(BIT_LENGTH)
    q = p
    while (q == p):
        q = number.getPrime(BIT_LENGTH)
    n = p * q
    phi_n = (p - 1) * (q - 1)
    e = E
    d = pow(e, -1, phi_n)
    return {
        "public": {"e": e, "n": n},
        "private": {"d": d, "n": n}
    }

def encrypt_message(message: int, public_key):
    if message >= public_key["n"]:
        raise ValueError("Message \"{}\" length exceeds maximum size {}".format(
            message, public_key["n"]
        ))
    return pow(message, public_key["e"], public_key["n"])

def decrypt_message(message: int, private_key):
    return pow(message, private_key["d"], private_key["n"])

def compare_io(keys, message):
    cypher = encrypt_message(message, keys["public"])
    decrypted = decrypt_message(cypher, keys["private"])
    print("Message {} encrypted to {}\nEncryption decrypted to {}".format(
        message, cypher, decrypted
    ))
    print("Original plaintext {} the decrypted plaintext.\n".format("matches" if message == decrypted else "does not match"))

def pkcs7(plaintext):
    if type(plaintext) == str:
        plaintext = bytes(plaintext, 'utf-8')
    bytes_to_add = 16 - (len(plaintext) % 16)
    padding_value_bin = chr(bytes_to_add).encode() # chr converts int to ASCII character
    if (len(plaintext) % 16 != 0):
        plaintext = plaintext + (padding_value_bin * bytes_to_add)
    return plaintext

def rsa_attack(key, message):
    # shared values
    # public key
    iv = get_random_bytes(AES.block_size)
    byte_len = 16

    # bob
    s1 = random.randint(0, key["public"]["n"])
    c = pow(s1, key["public"]["e"], key["public"]["n"])
    print("Bob sends value of c={} to Alice\n".format(c))

    # mallory
    # Replace c with 1
    cprime = 1
    print("Mallory intercepts the value of c and changes it to c'=1\n")

    #alice
    s2 = pow(cprime, key["private"]["d"], key["private"]["n"]) 
    alice_key = hashlib.sha256(s2.to_bytes((s2.bit_length() + 7) // 8, sys.byteorder)).hexdigest()[:byte_len]
    alice_cipher = AES.new(alice_key, AES.MODE_CBC, IV=iv)
    encrypted_message = alice_cipher.encrypt(pkcs7(message))
    print("Alice's s value will now always equal 1\n")
    print("Original message from Alice:\n{}\n".format(message))
    print("Encrypted message from Alice:\n{}\n".format(encrypted_message))

    # mallory
    s3 = 1
    mallory_key = hashlib.sha256(s3.to_bytes((s3.bit_length() + 7) // 8, sys.byteorder)).hexdigest()[:byte_len]
    mallory_cipher = AES.new(mallory_key, AES.MODE_CBC, IV=iv)
    decrypted_message = mallory_cipher.decrypt(encrypted_message)
    print("Decrypted message using s=1 to make a new key:\n{}\n".format(decrypted_message))

# %%
compare_io(get_rsa_keys(), 69420)
compare_io(get_rsa_keys(), 12345)
compare_io(get_rsa_keys(), 4568465832748297592)

# %%
rsa_attack(get_rsa_keys(), "Hi Bob!")


# %%