# %%
from Crypto.Cipher import AES 
from Crypto.Random import get_random_bytes
from pathlib import Path
import os
import sys
python_version = sys.version_info
if (python_version.major == 3 and python_version.minor > 7):
    import time # PyCryptodome library uses time.clock as dependency, but
    time.clock = time.time # time.clock was depricated in Python 3.8

KEY_LENGTH_BYTES = 16 # 128 bits
BMP_HEADER_SIZE_BYTES = 56 # standard header size, try 138 if it doesn't work
FILEPATH = "./mustang.bmp"

# %%
get_filetype = lambda FILEPATH : Path(FILEPATH).suffix
get_filesize_bytes = lambda FILEPATH : os.stat(FILEPATH).st_size
generate_key = lambda byte_count : get_random_bytes(byte_count)

def read_plaintext_bin(FILEPATH):
    with open(FILEPATH, "rb") as plaintext_file:
        return plaintext_file.read(get_filesize_bytes(FILEPATH))

def write_ciphertext_bin(FILEPATH, filedata): 
    with open(FILEPATH, "wb") as new_file:
        new_file.write(filedata)

def generate_initialization_vector(key):
    iv = key
    while iv == key:
        iv = get_random_bytes(AES.block_size)
    return iv

def pkcs7(plaintext):
    bytes_to_add = 16 - (len(plaintext) % 16)
    padding_value_bin = chr(bytes_to_add).encode() # chr converts int to ASCII character
    if (len(plaintext) % 16 != 0):
        plaintext = plaintext + (padding_value_bin * bytes_to_add)
    return plaintext

def separate_header(plaintext, header_size_bytes):
    return {
        "header": plaintext[0:header_size_bytes],
        "data": plaintext[header_size_bytes:]
    }

def xor_bytes(a, b):
    a_int = int.from_bytes(a, sys.byteorder)
    b_int = int.from_bytes(b, sys.byteorder)
    x = a_int ^ b_int
    return x.to_bytes(len(a) if len(a) >= len(b) else len(b), sys.byteorder)

def ecb_encryption(plaintext, key):
    plaintext = pkcs7(plaintext)
    cipher = AES.new(key, AES.MODE_ECB)
    ciphertext = b""
    block_count = len(plaintext) // AES.block_size
    for block in range(block_count):
        index1 = block * AES.block_size
        index2 = index1 + AES.block_size
        ciphertext = ciphertext + cipher.encrypt(plaintext[index1 : index2])
    return ciphertext

def cbc_encryption(plaintext, key, iv):
    plaintext = pkcs7(plaintext)
    cipher = AES.new(key, AES.MODE_ECB)
    ciphertext = b""
    last_encryption = iv
    block_count = len(plaintext) // AES.block_size
    for block in range(block_count):
        index1 = block * AES.block_size
        index2 = index1 + AES.block_size
        last_encryption = cipher.encrypt(xor_bytes(last_encryption, plaintext[index1 : index2]))
        ciphertext = ciphertext + last_encryption
    return ciphertext

# %%
def task1():
    if (get_filetype(FILEPATH) == ".bmp"):
        plaintext_bin = read_plaintext_bin(FILEPATH)
        bmp = separate_header(plaintext_bin, BMP_HEADER_SIZE_BYTES)
        
        ecb_key = generate_key(KEY_LENGTH_BYTES)
        write_ciphertext_bin(
            "mustang_ecb.bmp",
            bmp["header"] + ecb_encryption(bmp["data"], ecb_key)
        )

        cbc_key = generate_key(KEY_LENGTH_BYTES)
        cbc_iv = generate_initialization_vector(cbc_key)
        write_ciphertext_bin(
            "mustang_cbc.bmp",
            bmp["header"] + cbc_encryption(bmp["data"], cbc_key, cbc_iv)
        )

task1()
# %%
