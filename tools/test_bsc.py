#!/usr/bin/env python3
from web3 import Web3
from load_contract import load_contract

MY_WALLET_ADDRESS = "0x8D82Fef0d77d79e5231AE7BFcFeBA2bAcF127E2B"

bsc_w3 = Web3(Web3.HTTPProvider('https://bsc-dataseed1.binance.org:443'))

try:
    bsc_call=load_contract("0x4076CC26EFeE47825917D0feC3A79d0bB9a6bB5c", bsc_w3).claimableRewards(MY_WALLET_ADDRESS).call()
    bsc_call2=load_contract("0x4076CC26EFeE47825917D0feC3A79d0bB9a6bB5c", bsc_w3).lockedBalances(MY_WALLET_ADDRESS).call()
    print(round(bsc_call[0][1]/10**18,2), "EPS claimable")
    print(round(bsc_call[1][1]/10**18,2), "BUSD")
    print(round(bsc_call2[0]/10**18,2), "EPS locked")
except Exception:
    print("\nBSC networking error")
