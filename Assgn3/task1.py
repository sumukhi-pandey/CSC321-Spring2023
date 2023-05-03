# %%
import hashlib
import matplotlib.pyplot as plt
import math
import pandas as pd
import random
import string
import sys
import time

CHAR_LIST = string.ascii_uppercase + string.ascii_lowercase + string.digits

# %%
truncate = lambda hex_string, bit_length: int(bin(int(hex_string, 16))[:bit_length + 2], 2)

def hash_sha256(plain):
    if type(plain) == int:
        return hashlib.sha256(plain.to_bytes((plain.bit_length() + 7) // 8, sys.byteorder)).hexdigest()
    elif type(plain) == str:
        return hashlib.sha256(plain.encode()).hexdigest()
    else:
        return 0 

def get_random_string():
    length = random.randint(1, 10)
    return ''.join(random.choices(
        string.ascii_uppercase + string.ascii_lowercase + string.digits, 
        k=length
    ))

def birthday_attack(bit_length, probability):
    value_count = pow(2 * pow(2, bit_length) * math.log(1 / (1 - probability)), 0.5)
    strings = {truncate(hash_sha256(""), bit_length): "" }
    return_object = {
        "String 1": "ATTACK FAILED",
        "String 2": "ATTACK FAILED",
        "Inputs": 0,
        "Seconds": -time.time()
    }
    while len(strings) < value_count:
        new_string = get_random_string()
        new_hash = truncate(hash_sha256(new_string), bit_length)
        if new_hash in strings.keys():
            if strings[new_hash] != new_string:
                return_object["String 1"] = strings[new_hash]
                return_object["String 2"] = new_string
                break
        else:
            strings[new_hash] = new_string
            return_object["Inputs"] += 1
    return_object["Seconds"] += time.time()
    return return_object    

def graph(df, column):
    df[column].plot(
        kind="line", 
        title="Birthday Attack: {} vs Digest Size".format(column),
        xticks=range(df.index[0], df.index[-1] + 1, 2),
        xlabel="Digest Size in Bits",
    )
    plt.ylabel(column, rotation=0, ha='right')
    plt.show()

def task1b(str1, str2):
    print("Hamming distance: {}".format(
        sum(s1 != s2 for s1, s2 in zip(str1, str2))
    ))
    print("{}: {}\n{}: {}\n".format(
        str1, hash_sha256(str1),
        str2, hash_sha256(str2)
    ))

def task1c(min_bit_size, max_bit_size):
    df = pd.DataFrame(
        index=range(min_bit_size, max_bit_size + 1, 2),
        columns=["String 1", "String 2", "Inputs", "Seconds"]
    )
    print("[String 1, String 2, Input Count, Seconds Elapsed]")
    for i in df.index:
        results = birthday_attack(i, 0.999)
        df["String 1"][i] = results["String 1"]
        df["String 2"][i] = results["String 2"]
        df["Inputs"][i] = results["Inputs"]
        df["Seconds"][i] = results["Seconds"]
        print("{}: {}".format(i, df.loc[i].tolist()))
    return df
    

# %%
print("Task 1b:\n")
task1b("hello","heylo")
task1b("cameron","Cameron")
task1b("abcdef1","abcdefgh")

# %%
print("Task 1c:\n")
attack_df = task1c(8, 50)
attack_df

# graph(attack_df, "Inputs")
# graph(attack_df, "Seconds")

# truncate(hash_sha256(""), )
# %%