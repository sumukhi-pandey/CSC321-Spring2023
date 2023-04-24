# %%
from Crypto.Cipher import AES 
from Crypto.Random import get_random_bytes
import sys
import random
import hashlib
python_version = sys.version_info
if (python_version.major == 3 and python_version.minor > 7):
    import time # PyCryptodome library uses time.clock as dependency, but
    time.clock = time.time # time.clock was depricated in Python 3.8

# %%
# def truncate(integer, byte_length):
#     hex_val = pow(16, byte_length) - 1
#     return integer & hex_val

def pkcs7(plaintext):
    if type(plaintext) == str:
        plaintext = bytes(plaintext, 'utf-8')
    bytes_to_add = 16 - (len(plaintext) % 16)
    padding_value_bin = chr(bytes_to_add).encode() # chr converts int to ASCII character
    if (len(plaintext) % 16 != 0):
        plaintext = plaintext + (padding_value_bin * bytes_to_add)
    return plaintext

def dh_key(q, a):
    if type(q) == tuple:
        q = q[0]
    if type(a) == tuple:
        a = a[0]

    Xa = random.randint(0, q)
    Ya = pow(a, Xa, q)

    Xb = random.randint(0, q)
    Yb = pow(a, Xb, q)

    s1 = pow(Yb, Xa, q)
    s2 = pow(Ya, Xb, q)

    byte_len = 16
    k1 = hashlib.sha256(s1.to_bytes((s1.bit_length() + 7) // 8, sys.byteorder)).hexdigest()[:byte_len]
    k2 = hashlib.sha256(s2.to_bytes((s2.bit_length() + 7) // 8, sys.byteorder)).hexdigest()[:byte_len]
    return k1, k2

def pass_message(sender_message, sender_key, receiver_key):
    iv = get_random_bytes(AES.block_size)

    sender_cipher = AES.new(sender_key, AES.MODE_CBC, IV=iv)
    receiver_cipher = AES.new(receiver_key, AES.MODE_CBC, IV=iv)

    encrypted_message = sender_cipher.encrypt(pkcs7(sender_message))
    print("Encrypting message \"{}\"\nwith key {}\nResult: {}\n".format(sender_message, sender_key, encrypted_message))
    decrypted_message = receiver_cipher.decrypt(encrypted_message)
    print("Decrypting message \"{}\"\nwith key {}\nResult: {}\n\n".format(encrypted_message, receiver_key, decrypted_message))

# %%
k1, k2 = dh_key(
    q=0xB10B8F96A080E01DDE92DE5EAE5D54EC52C99FBCFB06A3C69A6A9DCA52D23B616073E28675A23D189838EF1E2EE652C013ECB4AEA906112324975C3CD49B83BFACCBDD7D90C4BD7098488E9C219A73724EFFD6FAE5644738FAA31A4FF55BCCC0A151AF5F0DC8B4BD45BF37DF365C1A65E68CFDA76D4DA708DF1FB2BC2E4A4371, 
    a=0xA4D1CBD5C3FD34126765A442EFB99905F8104DD258AC507FD6406CFF14266D31266FEA1E5C41564B777E690F5504F213160217B4B01B886A5E91547F9E2749F4D7FBD7D3B9A92EE1909D0D2263F80A76A6A24C087A091F531DBF0A0169B6A28AD662A4D18E73AFA32D779D5918D08BC8858F4DCEF97C2A24855E6EEB22B3B2E5
)

print("Key 1: {}\nKey 2: {}\n{} equal.\n\n".format(k1, k2, "are" if k1 == k2 else "are not"))

pass_message("Hi Bob!", k1, k2)
pass_message("Hi Alice!", k2, k1)
# %%
