from bcrypt import *

with open('shadow.txt') as f:
    pwd_list = f.read().splitlines()

with open('words.txt') as f:
    word_list = f.read().splitlines()

for pwd in pwd_list:
    hash = bytes(pwd[pwd.index(":") + 1 :], encoding='utf-8')


    pwd_details = {}


    pwd_parts = pwd.split('$')

    pwd_details['User'] = pwd_parts[0][: pwd_parts[0].index(':')]
    pwd_details['Alg'] = pwd_parts[1]
    pwd_details['WrkFac'] = pwd_parts[2]
    pwd_details['Salt'] = pwd_parts[3][:22]
    pwd_details['Hash'] = pwd_parts[3][22:]

    salt = "$" + pwd_details['Alg'] + "$" + pwd_details['WrkFac'] + "$" + pwd_details['Salt']
    salt = bytes(salt, encoding='utf-8')

    for word in word_list:
        if hashpw(bytes(word, encoding='utf-8'), salt) == hash:
            print(pwd_details['User'] + " has password " + word)
            break
