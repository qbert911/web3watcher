#!/usr/bin/env python3
from web3 import Web3
import json

MY_WALLET_ADDRESS = "0x8D82Fef0d77d79e5231AE7BFcFeBA2bAcF127E2B"

abieps = json.load(open("abi_4076.json", 'r'))
bsc_w3 = Web3(Web3.HTTPProvider('https://bsc-dataseed1.binance.org:443'))

try:
    bsc_call=bsc_w3.eth.contract("0x4076CC26EFeE47825917D0feC3A79d0bB9a6bB5c", abi=abieps).functions.claimableRewards(MY_WALLET_ADDRESS).call()
    bsc_call2=bsc_w3.eth.contract("0x4076CC26EFeE47825917D0feC3A79d0bB9a6bB5c", abi=abieps).functions.lockedBalances(MY_WALLET_ADDRESS).call()
    print(round(bsc_call[0][1]/10**18,2), "EPS claimable")
    print(round(bsc_call[1][1]/10**18,2), "BUSD")
    print(round(bsc_call2[0]/10**18,2), "EPS locked")
except:
    print("\nBSC networking error")
