#!/usr/bin/env python3
from web3 import Web3
from load_contract import load_contract

MY_WALLET_ADDRESS = "0x8D82Fef0d77d79e5231AE7BFcFeBA2bAcF127E2B"
INFURA_ID = "1d651358519346beb661128bf65ab651"
infura_w3 = Web3(Web3.HTTPProvider('https://mainnet.infura.io/v3/'+INFURA_ID))

sushi_call=load_contract("0xEF0881eC094552b2e128Cf945EF17a6752B4Ec5d", infura_w3).pendingSushi(1,MY_WALLET_ADDRESS).call()
sushi_call3=load_contract("0x9e01aaC4b3e8781a85b21d9d9F848e72Af77B362", infura_w3).earned(MY_WALLET_ADDRESS).call()
sushi_call4=load_contract("0x9e01aaC4b3e8781a85b21d9d9F848e72Af77B362", infura_w3).sushiBalanceOf(MY_WALLET_ADDRESS).call()


print(round(sushi_call4/10**18,8), "sushi lp tokens owned")
print(round(sushi_call/10**18,8), "sushi claimable")
print(round(sushi_call3/10**18,8), "cvx claimable")
