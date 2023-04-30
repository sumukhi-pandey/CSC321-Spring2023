# %%
import hashlib
import matplotlib.pyplot as plt
import pandas as pd
import random
import string
import sys
import time

# %%
truncate = lambda string, length: string[:length]

def hash_sha256(plain):
    if type(plain) == int:
        return hashlib.sha256(plain.to_bytes((plain.bit_length() + 7) // 8, sys.byteorder)).hexdigest()
    elif type(plain) == str:
        return hashlib.sha256(plain.encode()).hexdigest()
    else:
        return 0 

def get_random_string():
    length = random.randint(1, 21)
    return ''.join(random.choices(
        string.ascii_uppercase + string.ascii_lowercase + string.digits, 
        k=length
    ))

def birthday_attack(string, truncate_limit):
    new_string = ''
    digest = truncate(hash_sha256(string), truncate_limit)
    compare = truncate(hash_sha256(new_string), truncate_limit)
    used = {string}
    counter = 0
    start_time = time.time()
    while digest != compare:
        new_string = get_random_string()
        if new_string not in used:
            used.add(new_string)
            compare = truncate(hash_sha256(new_string), truncate_limit)
            counter += 1
    return {
        "String": new_string,
        "Inputs": counter,
        "Seconds": time.time() - start_time
    }

def graph(df, column):
    df[column].plot(
        kind="line", 
        title="{} vs Digest Size".format(column),
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

def task1c(string, min_bit_size, max_bit_size):
    df = pd.DataFrame(
        index=range(min_bit_size, max_bit_size + 1, 2),
        columns=["String", "Inputs", "Seconds"]
    )
    for i in df.index:
        results = birthday_attack(string, i)
        df["String"][i] = results["String"]
        df["Inputs"][i] = results["Inputs"]
        df["Seconds"][i] = results["Seconds"]
    return df
    

# %%
print("Task 1b:\n")
task1b("hello","heylo")
task1b("cameron","Cameron")
task1b("abcdef1","abcdefgh")

# %%
print("Task 1c:\n")
attack_df = task1c("Cameron", 8, 50)
graph(attack_df, "Inputs")
graph(attack_df, "Seconds")

# %%