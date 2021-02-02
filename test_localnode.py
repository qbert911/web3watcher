#!/usr/bin/env python3
from web3 import Web3, HTTPProvider

# https://dappnode.github.io/DAppNodeDocs/what-can-you-do/

rpc = 'http://geth.dappnode:8545'



INFURA_ID = "6aa1a043a9854eaa9fa68d17f619f326"
w3 = Web3(Web3.HTTPProvider('https://mainnet.infura.io/v3/'+INFURA_ID))
web3_rpc = Web3(HTTPProvider('http://172.33.0.2:8545'))
print(web3_rpc.isConnected()) # False
print(str(w3.eth.gasPrice))
print(str(web3_rpc.eth.gasPrice))
