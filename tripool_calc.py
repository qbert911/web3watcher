#!/usr/bin/env python3
"""tripool functions"""
# pylint: disable=C0103,C0116,C0301,W0105,E0401,R0914
import json
import argparse
from colorama import Fore, Style, init
from web3 import Web3
init()
purchase_array = [{"dollar_value":11000, "tokens_recieved":  8.26260, "btc_price": 37665, "eth_price":2233},
                  {"dollar_value":18854, "tokens_recieved": 16.17576, "btc_price": 31968, "eth_price":1828},
                  {"dollar_value": 5160, "tokens_recieved":  3.91480, "btc_price": 35391, "eth_price":2351}]
#4.16434270 last_prices.....
#https://etherscan.io/tx/0xc5b9f3fdc0b1421b3030d7a253e728dfd1136e3c5475ba0f1c7e7e157779e5e6  #tripool entrance 1
MY_WALLET_ADDRESS = "0x8D82Fef0d77d79e5231AE7BFcFeBA2bAcF127E2B"
INFURA_ID = "bfdd3973b810492db7cb27792702782f"
infura_w3 = Web3(Web3.HTTPProvider('https://mainnet.infura.io/v3/'+INFURA_ID))

abiguage = json.load(open("abi/abi_6955.json", 'r'))
abiswap = json.load(open("abi/abi_8046.json", 'r'))
#abiyvault = json.load(open("abi/abi_3d98.json", 'r'))

tri_guage = infura_w3.eth.contract("0x6955a55416a06839309018A8B0cB72c4DDC11f15", abi=abiguage).functions
tri_swap = infura_w3.eth.contract("0x80466c64868E1ab14a1Ddf27A676C3fcBE638Fe5", abi=abiswap).functions
#tri_yvault = infura_w3.eth.contract("0x3D980E50508CFd41a13837A60149927a11c03731", abi=abiyvault).functions

def tri_calc(fulldisplay, guage_bal):
    _all_dollars_spent = sum(item['dollar_value'] for item in purchase_array)
    labels = ['usd', 'btc', 'eth']
    decimals = [6, 8, 18]
    _curr_val = _return_total = sim_total = 0
    buf = ""
    _coins = []
    _price_oracle = [1,0,0]
    if guage_bal < 1:
        guage_bal = tri_guage.balanceOf(MY_WALLET_ADDRESS).call()
    totalSupply = tri_guage.totalSupply().call()
    virt_price = tri_swap.get_virtual_price().call()/10**18
    #virt_string = f"{10000000*((virt_price)-1): 5.0f}"
    if fulldisplay:
        parser2 = argparse.ArgumentParser()
        parser2.add_argument("-e", "--Ethvalue", type=int, help="Theoretical ETH value")
        parser2.add_argument("-b", "--Btcvalue", type=int, help="Theoretical BTC value")
        args2 = parser2.parse_args()
        if args2.Ethvalue:
            _price_oracle[2] = args2.Ethvalue
        if args2.Btcvalue:
            _price_oracle[1] = args2.Btcvalue
    for i in range(3):
        if i > 0 and _price_oracle[i] < 1:
            #_price_oracle[i] = (tri_swap.price_scale(i - 1).call() + tri_swap.last_prices(i - 1).call() + tri_swap.price_oracle(i - 1).call())/3/ 10 ** 18
            #_price_oracle[i] = tri_swap.last_prices(i - 1).call()/ 10 ** 18
            _price_oracle[i] = tri_swap.price_oracle(i - 1).call()/ 10 ** 18

        if fulldisplay:
            _allthiscoin = tri_swap.balances(i).call()/ 10 ** decimals[i]
            _coins.append( guage_bal / totalSupply * _allthiscoin )
            _val = _coins[i] * _price_oracle[i]
            _curr_val += _val
            buf+=(f"         {labels[i]}: ${_val:06,.0f} ={_coins[i]: 12.5f} @ "+Fore.CYAN+f"${_price_oracle[i]:,.2f}\n"+Style.RESET_ALL)

    if fulldisplay:
        thiscolor = Fore.RED+Style.BRIGHT
        if _all_dollars_spent < _curr_val:
            thiscolor = Fore.GREEN+Style.BRIGHT
        print(f"   virtprice: {virt_price}\n"+f"Total supply: {totalSupply / 10 ** 18:,.0f}\n"+f" Tokens held: {guage_bal / 10 ** 18:.4f}\n")

    for j in range(len(purchase_array)):
        x = _price_oracle[1] / purchase_array[j]["btc_price"]
        y = _price_oracle[2] / purchase_array[j]["eth_price"]
        z = (x+y+1) / 3
        sim_total += z * purchase_array[j]['dollar_value']
        if fulldisplay:
            print(f"Purchase #{j+1: 2d}: $"+Fore.GREEN+f"{purchase_array[j]['dollar_value']:06,d}"+Style.RESET_ALL, end = "")
            print("  for  ©"+Fore.MAGENTA+f"{purchase_array[j]['tokens_recieved']:5.2f}"+Style.RESET_ALL+f"      ${purchase_array[j]['dollar_value']/purchase_array[j]['tokens_recieved']:.0f}", end = "   ")
            print("Actual ["+Fore.CYAN+f"{((_curr_val/(guage_bal/10**18)/(purchase_array[j]['dollar_value']/purchase_array[j]['tokens_recieved']))-1)*100:6.2f}"+Style.RESET_ALL+"%]", end = "  ")
            print("Sim ["+Fore.CYAN+Style.BRIGHT+f"{(z-1)*100:6.2f}"+Style.RESET_ALL+"%] "+f"BTC[{(x-1) * 100:6.2f}%] ETH[{(y-1) * 100:6.2f}%]")
            #print(" "*44,"Simulated ["+Fore.CYAN+Style.BRIGHT+f"{(z-1)*100:6.2f}"+Style.RESET_ALL+"%]"+Style.RESET_ALL)  #= worth $"+Fore.YELLOW+f"{z * purchase_array[j]['dollar_value']:5.0f}
    if fulldisplay:
        print(" "*3,"Invested: $"+Fore.GREEN+f"{_all_dollars_spent:,.0f}"+Style.RESET_ALL+" (Each "+Fore.MAGENTA+"©"+Style.RESET_ALL+f"token was: ${_all_dollars_spent/(guage_bal/10**18):.0f})\n")
        print(buf, end="")
        print(" "*6,"Total: $"+Fore.YELLOW+Style.BRIGHT+f"{_curr_val:,.0f}"+Style.RESET_ALL+" (Each "+Fore.MAGENTA+"©"+Style.RESET_ALL+"token now: $"+thiscolor+f"{_curr_val/(guage_bal/10**18):.0f}"+Style.RESET_ALL+") Change: ["+Fore.CYAN+f"{100*((_curr_val/_all_dollars_spent)-1):6.2f}"+Style.RESET_ALL+"%]\n")
        print(" "*2,"Simulated: $"+Fore.YELLOW+f"{sim_total:,.0f}"+Style.RESET_ALL+" (Each "+Fore.MAGENTA+"©"+Style.RESET_ALL+f"token was: ${sim_total/(guage_bal/10**18):.0f}) Simula: ["+Fore.CYAN+Style.BRIGHT+f"{100*((sim_total/_all_dollars_spent)-1):6.2f}"+Style.RESET_ALL+"%]")

        #print(" "*1,f"Value Diff: ${_curr_val - _all_dollars_spent:6,.0f} = $"+Fore.YELLOW+Style.BRIGHT+f"{_curr_val:,.0f}"+Style.RESET_ALL+" - $"+Fore.GREEN+f"{_all_dollars_spent:,.0f}"+Style.RESET_ALL)
        #print(" "*1,f"Value Diff: ${sim_total - _all_dollars_spent:6,.0f} = $"+Fore.YELLOW+f"{sim_total:,.0f}"+Style.RESET_ALL+" - $"+Fore.GREEN+f"{_all_dollars_spent:,.0f}"+Style.RESET_ALL)

        #a = tri_yvault.balanceOf(MY_WALLET_ADDRESS).call()/10**18
        #b = tri_yvault.totalSupply().call()/10**18
        #c = tri_yvault.pricePerShare().call()/10**18
        #d = tri_yvault.totalAssets().call()/10**18
        #print("Yvault supply: ",a,b,c,d, b*c,b*_curr_val/(guage_bal/10**18))
        #print(,,100*((/_all_dollars_spent)-1))
    else:
        print("["+Fore.CYAN+Style.BRIGHT+f"{100*((sim_total/_all_dollars_spent)-1):.2f}"+Style.RESET_ALL+"%]",end='')

    return sim_total

if __name__ == "__main__":
    print(tri_calc(True,0))

    print(tri_calc(False,0))
