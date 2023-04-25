# %%
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

def dh_key_attack_1(q, a):
    Xa = random.randint(0, q)
    Ya = pow(a, Xa, q)

    Xb = random.randint(0, q)
    Yb = pow(a, Xb, q)

    # Attack
    Ya = q
    Yb = q

    s1 = pow(Yb, Xa, q)
    s2 = pow(Ya, Xb, q)

    byte_len = 16
    k1 = hashlib.sha256(s1.to_bytes((s1.bit_length() + 7) // 8, sys.byteorder)).hexdigest()[:byte_len]
    k2 = hashlib.sha256(s2.to_bytes((s2.bit_length() + 7) // 8, sys.byteorder)).hexdigest()[:byte_len]
    return k1, k2

def dh_key_attack_2(q, a, new_a):
    # attack
    a = new_a

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

# %%
q=0xB10B8F96A080E01DDE92DE5EAE5D54EC52C99FBCFB06A3C69A6A9DCA52D23B616073E28675A23D189838EF1E2EE652C013ECB4AEA906112324975C3CD49B83BFACCBDD7D90C4BD7098488E9C219A73724EFFD6FAE5644738FAA31A4FF55BCCC0A151AF5F0DC8B4BD45BF37DF365C1A65E68CFDA76D4DA708DF1FB2BC2E4A4371
a=0xA4D1CBD5C3FD34126765A442EFB99905F8104DD258AC507FD6406CFF14266D31266FEA1E5C41564B777E690F5504F213160217B4B01B886A5E91547F9E2749F4D7FBD7D3B9A92EE1909D0D2263F80A76A6A24C087A091F531DBF0A0169B6A28AD662A4D18E73AFA32D779D5918D08BC8858F4DCEF97C2A24855E6EEB22B3B2E5

# %%
k1, k2 = dh_key_attack_1(q, a)
stolen_key = hashlib.sha256(b'').hexdigest()[:16]
print("Modifying YA and YB to q:\nKeys 1 & 2: {}\nStolen key: {}\n{} equal.".format(
    k1, stolen_key, "are" if k1 == stolen_key else "are not"
))

# %%
k1, k2 = dh_key_attack_2(q, a, 1)
stolen_key = hashlib.sha256(b'\x01').hexdigest()[:16]
print("Modifying \\alpha to 1:\nKeys 1 & 2: {}\nStolen key: {}\n{} equal.".format(
    k1, stolen_key, "are" if k1 == stolen_key else "are not"
))

# %%
k1, k2 = dh_key_attack_2(q, a, q)
stolen_key = hashlib.sha256(b'').hexdigest()[:16]
print("Modifying \\alpha to q:\nKeys 1 & 2: {}\nStolen key: {}\n{} equal.".format(
    k1, stolen_key, "are" if k1 == stolen_key else "are not"
))

# %%
k1, k2 = dh_key_attack_2(q, a, q - 1)
stolen_key = hashlib.sha256(b'\x01').hexdigest()[:16]
print("Modifying \\alpha to q - 1:\nKeys 1 & 2: {}\nStolen key: {}\n{} equal.".format(
    k1, stolen_key, "are" if k1 == stolen_key else "are not"
))

# %%
