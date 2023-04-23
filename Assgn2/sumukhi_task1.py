from Crypto.Cipher import AES 
from Crypto.Random import get_random_bytes
from pathlib import Path
import os
import sys
import random
import hashlib
import secrets

q = 37
a = 5


def dhKey():
    Xa = random.randint(0, q)
    Ya = (a ** Xa) % q

    Xb = random.randint(0, q)
    Yb = (a ** Xb) % q

    s1 = (Yb ** Xa) % q
    s2 = (Ya ** Xb) % q

    k1 = hashlib.sha256(s1.to_bytes(16, "big")).hexdigest()
    k2 = hashlib.sha256(s2.to_bytes(16, "big")).hexdigest()

    print(secrets.compare_digest(k1, k2))


def main():
    dhKey()

if __name__ == "__main__":  
    main()