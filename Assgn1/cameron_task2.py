# %%
from Crypto.Cipher import AES 
from Crypto.Random import get_random_bytes
import random
import string
import sys
import urllib.parse
python_version = sys.version_info
if (python_version.major == 3 and python_version.minor > 7):
    import time # PyCryptodome library uses time.clock as dependency, but
    time.clock = time.time # time.clock was depricated in Python 3.8

KEY_LENGTH_BYTES = 16 # 128 bits
KEY = get_random_bytes(KEY_LENGTH_BYTES)

def generate_initialization_vector(key):
    iv = key
    while iv == key:
        iv = get_random_bytes(AES.block_size)
    return iv
IV = generate_initialization_vector(KEY)

# %%
def pkcs7(plaintext):
    bytes_to_add = 16 - (len(plaintext) % 16)
    padding_value_bin = chr(bytes_to_add).encode() # chr converts int to ASCII character
    if (len(plaintext) % 16 != 0):
        plaintext = plaintext + (padding_value_bin * bytes_to_add)
    return plaintext

def xor_bytes(a, b):
    a_int = int.from_bytes(a, sys.byteorder)
    b_int = int.from_bytes(b, sys.byteorder)
    x = a_int ^ b_int
    return x.to_bytes(len(a) if len(a) >= len(b) else len(b), sys.byteorder)

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

def submit(user_string):
    formatted_string = "userid=456; userdata={};session-id=31337".format(user_string)
    url_string = urllib.parse.quote(formatted_string)
    padded_bin_string = pkcs7(bytes(url_string, 'utf-8'))
    return cbc_encryption(padded_bin_string, KEY, IV)

def verify(ciphertext):
    cipher = AES.new(KEY, AES.MODE_CBC, IV=IV)
    decrypted_string = cipher.decrypt(ciphertext).decode("ISO-8859-1")
    return urllib.parse.unquote(decrypted_string)

def cbc_testcase(string, substring, truthiness):
    if (substring in string) != truthiness:
        raise Exception(
            "String \"{}\" containing substring \"{}\" does not match expected truthiness {}".format(
                string, substring, truthiness
        ))

def bitflip(ciphertext, target_block):
    for i in range(15, -1, -1):
        decrypted = verify(ciphertext)
        block_input = ciphertext[i] ^ ord(decrypted[i + AES.block_size])
        replacement = block_input ^ ord(target_block[i])
        ciphertext = ciphertext[:i] + replacement.to_bytes(
            (replacement.bit_length() + 7) // 8,
            sys.byteorder
        ) + ciphertext[i + 1:]
    return ciphertext

# %%
def task2():
    substr = ";admin=true;"
    cbc_testcase(verify(submit("blahblahblah;admin=true;datadata")), substr, True)
    cbc_testcase(verify(submit("blahblahblah;admin=false;datadata")), substr, False)
    cbc_testcase(verify(submit("blahblahblah;admin=tru;datadata")), substr, False)
    cbc_testcase(verify(submit("blahblahblah;admin;=truedatadata")), substr, False)

task2()

# %% 
def task2_fun_part():
    success_count = 0
    tries = 1000
    target = ";admin=true;"
    for i in range(tries):
        try:
            input_str = ''.join(random.choice(string.printable) for x in range(32))
            verified = verify(bitflip(submit(input_str), target + "------"))
            success_count += 1
        except:
            pass

    print("Target \"{}\" successfully inserted through bit flip attack:\n{} out of {} times".format(target, success_count, tries))

task2_fun_part()
# %%
