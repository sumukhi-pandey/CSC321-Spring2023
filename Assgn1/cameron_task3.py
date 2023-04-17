#%%
import os
import matplotlib.pyplot as plt
import pandas as pd

# %%
def run_speed_tests():
    aes_speed = os.popen("openssl speed aes").read()
    rsa_speed = os.popen("openssl speed rsa").read()
    return aes_speed, rsa_speed

def get_aes_df(aes):
    df = pd.DataFrame([[val[:-1] for val in col.split()[2:]] for col in aes.split("\n")[6:-1]])
    df.rename(
        index={0:"aes-128 cbc", 1:"aes-192 cbc", 2:"aes-256 cbc"}, 
        columns={0:"16 bytes", 1:"64 bytes", 2:"256 bytes", 3:"1024 bytes", 4:"8192 bytes"},
        inplace=True)
    return df.astype("float").transpose()

def graph_aes(aes):
    aes.plot(
        kind="line",
        title="Block Size vs. AES Throughput",
        xlabel="Block Size",
    )
    plt.legend(title="AES Key Size", bbox_to_anchor=(1.0, 1.0))
    plt.ylabel("kB / second\nProcessed ", rotation='horizontal', ha='right')
    plt.savefig('task3_graph_aes.pdf')

def get_rsa_df(rsa):
    df = pd.DataFrame([col.split()[5:] for col in rsa.split("\n")[5:-1]])
    df.rename(
        index={0:"rsa 512 bits", 1:"rsa 1024 bits", 2:"rsa 2048 bits", 3:"rsa 4096 bits"},
        columns={0:"sign", 1:"verify", 2:"sign/second", 3:"verify/second"}, 
        inplace=True)
    return df.astype("float")

def graph_rsa(rsa):
    rsa.plot(
        kind="line",
        title="Key Size vs. RSA Throughput",
        xlabel="Key Size",
    )
    plt.legend(title="RSA Function", bbox_to_anchor=(1.0, 1.0))
    plt.ylabel("Operations /\nsecond     ", rotation='horizontal', ha='right')
    plt.savefig('task3_graph_rsa.pdf')

# %%
aes_speed, rsa_speed = run_speed_tests()
graph_aes(get_aes_df(aes_speed))
graph_rsa(get_rsa_df(rsa_speed))

# %%
