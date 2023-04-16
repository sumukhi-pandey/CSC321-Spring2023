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

KEY_LENGTH_BYTES = 32 # 256 bits
BMP_HEADER_SIZE_BYTES = 56 # standard header size, try 138 if it doesn't work

# %%
get_filetype = lambda filepath : Path(filepath).suffix
get_filesize_bytes = lambda filepath : os.stat(filepath).st_size
generate_key = lambda byte_count : get_random_bytes(byte_count)

def read_plaintext_bin(filepath):
    with open(filepath, "rb") as plaintext_file:
        return plaintext_file.read(get_filesize_bytes(filepath))

def write_ciphertext_bin(filepath, filedata): 
    with open(filepath, "wb") as new_file:
        new_file.write(filedata)

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

# %%
def task1():
    filepath = "./cp-logo.bmp"
    if (get_filetype(filepath) == ".bmp"):
        plaintext_bin = read_plaintext_bin(filepath)
        bmp = separate_header(plaintext_bin, BMP_HEADER_SIZE_BYTES)
        
        write_ciphertext_bin( # ECB
            "ecb_cameron_test3.bmp",
            bmp["header"] + ecb_encryption(bmp["data"], generate_key(KEY_LENGTH_BYTES))
        )

# %%
task1()
# %%
