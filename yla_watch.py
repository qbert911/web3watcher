#!/usr/bin/env python3
"""yla functions"""
# pylint: disable=C0103,C0116,C0301,W0105,E0401,R0914
import time
import json
from web3 import Web3

MY_WALLET_ADDRESS = "0x8D82Fef0d77d79e5231AE7BFcFeBA2bAcF127E2B"
INFURA_ID = "6aa1a043a9854eaa9fa68d17f619f326"
infura_w3 = Web3(Web3.HTTPProvider('https://mainnet.infura.io/v3/'+INFURA_ID))
abiyla = json.load(open("abi/abi_5f6f.json", 'r'))
abiy = json.load(open("abi/abi_a696.json", 'r'))
yfuncs = infura_w3.eth.contract("0x9ba60bA98413A60dB4C651D4afE5C937bbD8044B", abi=abiyla).functions

def yla_getvalue(printit):
    my_yla_tokens = yfuncs.balanceOf(MY_WALLET_ADDRESS).call()/10**18
    total_yla_supply = yfuncs.totalSupply().call()/10**18
    current_token_array = yfuncs.getCurrentTokens().call()
    my_pool_percent=my_yla_tokens/total_yla_supply
    totalvalue = 0
    for i in current_token_array:
        label = infura_w3.eth.contract(i, abi=abiy).functions.symbol().call()
        this_token_value = infura_w3.eth.contract(i, abi=abiy).functions.pricePerShare().call()/10**18
        this_token_amount_held_by_yla = yfuncs.getBalance(i).call()/10**18
        totalvalue+=this_token_value*this_token_amount_held_by_yla
        if printit:
            print(str(label).ljust(22), end= " ")
            print(str(this_token_value).ljust(20), end= " ")
            print(str(round(this_token_amount_held_by_yla)).rjust(9), end= " ")
            print(str(round(this_token_amount_held_by_yla*this_token_value)).rjust(9), end= " ")
            print(str(round(this_token_amount_held_by_yla*this_token_value*my_pool_percent)).rjust(6))

    if printit:
        month, day, hour, minut = map(str, time.strftime("%m %d %H %M").split())
        print("\nYearn Lazy Ape Report\n",month+"/"+day+" "+hour+":"+minut+"\n"+"-"*30)
        print(format(round(total_yla_supply), ',.0f'), "total tokens")
        print(round(my_yla_tokens), "tokens owned", end=" ")
        print("("+str(my_pool_percent*100),"% of pool owned)")

        print("$"+str(format(round(totalvalue), ',.0f')),"total value")
        print("$"+str(totalvalue*my_pool_percent),"my share")
        print("$"+str(totalvalue/total_yla_supply),"YLA token value","\n")

    return totalvalue*my_pool_percent

if __name__ == "__main__":
    a = yla_getvalue(True)
    print(a)
