#!/usr/bin/env python3
import time
from web3 import Web3, HTTPProvider

web3_rpc = Web3(HTTPProvider('http://192.168.0.4:8545'))
print(web3_rpc.isConnected())

while True:
    a = web3_rpc.eth.syncing
    if a is False:
        print("Local Node Done Syncing")
        break
    print(a['highestBlock']-a['currentBlock'], "blocks left to catch up")
    time.sleep(60)
