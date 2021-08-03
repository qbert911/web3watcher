#!/usr/bin/env python3
#pip install git+https://github.com/ethereum/web3.py@refs/pull/1411/merge   #need to install pull request code to add content function
from ens import ENS
import web3

def ipfs_hash_value(w3, website):
    return ENS.fromWeb3(w3).content(website)['hash']

if __name__ == "__main__":
    local_w3 = web3.Web3(web3.HTTPProvider('http://192.168.0.4:8545'))
    z = ipfs_hash_value(local_w3,'curve.eth')
    print(z)
