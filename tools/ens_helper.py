#!/usr/bin/env python3
from ens import ENS
from web3 import Web3

def ipfs_hash_value(w3, website, showerror=False):
    try:
        return ENS.fromWeb3(w3).content(website)['hash']
    except Exception as e:
        if showerror:
            print(e)
            print("need to install web3.py pull request via pip to get access to content function:")
            print("     pip3 install git+https://github.com/ethereum/web3.py@refs/pull/1411/merge")
        return

if __name__ == "__main__":
    INFURA_ID = "1d651358519346beb661128bf65ab651"
    infura_w3 = Web3(Web3.HTTPProvider('https://mainnet.infura.io/v3/'+INFURA_ID))
    #local_w3 = web3.Web3(web3.HTTPProvider('http://192.168.0.4:8545'))
    print(ipfs_hash_value(infura_w3,'curve.eth', True))
