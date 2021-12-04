#!/usr/bin/env python3
from web3 import Web3
from load_contract import load_contract
from price_getter import update_price

MY_WALLET_ADDRESS = "0x8D82Fef0d77d79e5231AE7BFcFeBA2bAcF127E2B"
INFURA_ID = "1d651358519346beb661128bf65ab651"
infura_w3 = Web3(Web3.HTTPProvider('https://mainnet.infura.io/v3/'+INFURA_ID))

sushi_call=load_contract("0xEF0881eC094552b2e128Cf945EF17a6752B4Ec5d", infura_w3).pendingSushi(1,MY_WALLET_ADDRESS).call()
sushi_call3=load_contract("0x9e01aaC4b3e8781a85b21d9d9F848e72Af77B362", infura_w3).earned(MY_WALLET_ADDRESS).call()

print(round(sushi_call/10**18,8), "sushi claimable")
print(round(sushi_call3/10**18,8), "cvx claimable\n")

tokens_owned=load_contract("0x9e01aaC4b3e8781a85b21d9d9F848e72Af77B362", infura_w3).sushiBalanceOf(MY_WALLET_ADDRESS).call()
slp_pool=load_contract("0x05767d9EF41dC40689678fFca0608878fb3dE906", infura_w3)
total_supply=slp_pool.totalSupply().call()
reserves=slp_pool.getReserves().call()
CVX = update_price("convex-finance",'','')
slp_token_value = 2 * reserves[0] * CVX / total_supply

print(round(tokens_owned/10**18,8), "sushi lp tokens owned")
print(round(total_supply/10**18,8), "sushi lp tokens total\n")
print(round(reserves[0]/10**18),"CVX in total")
print(round(reserves[1]/10**18),"ETH in total\n")

print(slp_token_value*round(tokens_owned/10**18,8),"stack worth\n")
print (slp_token_value, "token price\n")

x = round((tokens_owned / total_supply ) * reserves[0]/10**18)
y = round((tokens_owned / total_supply ) * reserves[1]/10**18,3)
print(x,"CVX owned")
print(y,"ETH owned")
