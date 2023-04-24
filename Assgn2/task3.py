# %%
from Crypto.Util import number
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

# %%
compare_io(get_rsa_keys(), 69420)
compare_io(get_rsa_keys(), 12345)
compare_io(get_rsa_keys(), 4568465832748297592)

# %%



# %%