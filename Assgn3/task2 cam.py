# %%
from bcrypt import *
import concurrent.futures
import multiprocessing as mp
import numpy as np
import time

# %%
def get_pwd_list(filename='shadow.txt'):
    with open(filename) as f:
        return f.read().splitlines()

def get_word_list(filename='words.txt'):
    with open(filename) as f:
        return f.read().splitlines()
    
def get_pwd_details(pwd_list):
    pwd_table = {}
    for pwd in pwd_list:
        colon_idx = pwd.index(":")
        pwd_table[pwd[1+colon_idx:].encode('utf-8')] = pwd[:colon_idx]
    return pwd_table

def get_crack_results(password, user, word_list):
    start_time = time.time()
    for word in word_list:
        if checkpw(word.encode('utf-8'), password):
            return {
                "user": user,
                "password": word,
                "seconds": time.time() - start_time
            }
    return False

def check_passwords(pwd_table, word_list):
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = [executor.submit(get_crack_results, pwd, pwd_table[pwd], word_list) for pwd in pwd_table.keys()]
        for future in futures:
            results = future.result()
            if results:
                print("{} password: {}.\nCracked in {} seconds.\n".format(
                    results["user"], results["password"], results["seconds"]
                ))

if __name__ == '__main__':
    PROCESS_COUNT = 4
    pwd_table = get_pwd_details(get_pwd_list())
    word_lists = np.array_split(get_word_list(), PROCESS_COUNT)

    with mp.Pool(processes=PROCESS_COUNT) as pool:
        arg_list = [(pwd_table, word_sublist) for word_sublist in word_lists]
        pool.starmap(check_passwords, arg_list)