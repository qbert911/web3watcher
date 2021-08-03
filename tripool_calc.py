#!/usr/bin/env python3
"""tripool functions"""
# pylint: disable=C0103,C0116,C0301,W0105,E0401,R0914
import argparse
from web3 import Web3
from colorama import Fore, Style, init
from tools.load_contract import load_contract
import convex_examiner
init()
purchase_array = [{"dollar_value":11000, "tokens_recieved":  8.2626, "btc_price": 37665, "eth_price":2233},
                  {"dollar_value":18854, "tokens_recieved": 16.1750, "btc_price": 31968, "eth_price":1828},
                  {"dollar_value": 5160, "tokens_recieved":  3.9146, "btc_price": 35391, "eth_price":2351}]

MY_WALLET_ADDRESS = "0x8D82Fef0d77d79e5231AE7BFcFeBA2bAcF127E2B"
INFURA_ID = "bfdd3973b810492db7cb27792702782f"   #bw-tricalc #"1d651358519346beb661128bf65ab651" #by-tricalc
infura_w3 = Web3(Web3.HTTPProvider('https://mainnet.infura.io/v3/'+INFURA_ID))


tri_guage = load_contract("0xDeFd8FdD20e0f34115C7018CCfb655796F6B2168",infura_w3)
tri_swap = load_contract("0xD51a44d3FaE010294C616388b506AcdA1bfAAE46",infura_w3)

def tri_calc(fulldisplay, guage_bal):
    _all_dollars_spent = sum(item['dollar_value'] for item in purchase_array)
    labels = ['usd', 'btc', 'eth']
    decimals = [6, 8, 18]
    _curr_val = _return_total = sim_total = 0
    buf = ""
    _coins = []
    _price_oracle = [1,0,0]
    if fulldisplay:
        parser2 = argparse.ArgumentParser()
        parser2.add_argument("-e", "--Ethvalue", type=int, help="Theoretical ETH value")
        parser2.add_argument("-b", "--Btcvalue", type=int, help="Theoretical BTC value")
        args2 = parser2.parse_args()
        if args2.Ethvalue:
            _price_oracle[2] = args2.Ethvalue
        if args2.Btcvalue:
            _price_oracle[1] = args2.Btcvalue
    try:
        if guage_bal < 1:
            _coins_in_covex_guage = convex_examiner.trix_getvalue(False,None,infura_w3)[0]
            guage_bal = tri_guage.balanceOf(MY_WALLET_ADDRESS).call() +(_coins_in_covex_guage*(10**18))
        totalSupply = tri_guage.totalSupply().call()
        virt_price = tri_swap.get_virtual_price().call()/10**18
        for i in range(3):
            if i > 0 and _price_oracle[i] < 1:
                _price_oracle[i] = tri_swap.price_oracle(i - 1).call()/ 10 ** 18

            if fulldisplay:
                _allthiscoin = tri_swap.balances(i).call()/ 10 ** decimals[i]
                _coins.append( guage_bal / totalSupply * _allthiscoin )
                _val = _coins[i] * _price_oracle[i]
                _curr_val += _val
                buf+=(f"         {labels[i]}: ${_val:06,.0f} ={_coins[i]: 12.5f} @ "+Fore.CYAN+f"${_price_oracle[i]:,.2f}\n"+Style.RESET_ALL)

        if fulldisplay:
            print(f"   virtprice: {virt_price}\n"+f"Total supply: {totalSupply / 10 ** 18:,.0f}\n"+f" Tokens held: {guage_bal / 10 ** 18:.4f}\n")

        for j in range(len(purchase_array)):
            x = _price_oracle[1] / purchase_array[j]["btc_price"]
            y = _price_oracle[2] / purchase_array[j]["eth_price"]
            z = (x+y+1) / 3
            sim_total += z * purchase_array[j]['dollar_value']
            if fulldisplay:
                thiscolor = Fore.RED+Style.BRIGHT
                if _all_dollars_spent < sim_total:
                    thiscolor = Fore.GREEN+Style.BRIGHT
                print(f"Purchase #{j+1: 2d}: $"+Fore.GREEN+f"{purchase_array[j]['dollar_value']:06,d}"+Style.RESET_ALL, end = "")
                print("  for  ©"+Fore.MAGENTA+f"{purchase_array[j]['tokens_recieved']:5.2f}"+Style.RESET_ALL+f"      ${purchase_array[j]['dollar_value']/purchase_array[j]['tokens_recieved']:.0f}", end = "   ")
                print("Actual ["+Fore.CYAN+f"{((_curr_val/(guage_bal/10**18)/(purchase_array[j]['dollar_value']/purchase_array[j]['tokens_recieved']))-1)*100:6.2f}"+Style.RESET_ALL+"%]", end = "  ")
                print("Sim ["+Fore.CYAN+Style.BRIGHT+f"{(z-1)*100:6.2f}"+Style.RESET_ALL+"%] "+f"BTC[{(x-1) * 100:6.2f}%] ETH[{(y-1) * 100:6.2f}%]")
                #print(" "*44,"Simulated ["+Fore.CYAN+Style.BRIGHT+f"{(z-1)*100:6.2f}"+Style.RESET_ALL+"%]"+Style.RESET_ALL)  #= worth $"+Fore.YELLOW+f"{z * purchase_array[j]['dollar_value']:5.0f}
        if fulldisplay:
            print(" "*3,"Invested: $"+Fore.GREEN+f"{_all_dollars_spent:,.0f}"+Style.RESET_ALL+" (Each "+Fore.MAGENTA+"©"+Style.RESET_ALL+f"token was: ${_all_dollars_spent/(guage_bal/10**18):.0f})\n")
            print(buf, end="")
            print(" "*6,"Total: $"+Fore.YELLOW+Style.BRIGHT+f"{_curr_val:,.0f}"+Style.RESET_ALL+" (Each "+Fore.MAGENTA+"©"+Style.RESET_ALL+"token now: $"+thiscolor+f"{_curr_val/(guage_bal/10**18):.0f}"+Style.RESET_ALL+") Change: ["+Fore.CYAN+f"{100*((_curr_val/_all_dollars_spent)-1):6.2f}"+Style.RESET_ALL+"%]\n")
            print(" "*2,"Simulated: $"+Fore.YELLOW+f"{sim_total:,.0f}"+Style.RESET_ALL+" (Each "+Fore.MAGENTA+"©"+Style.RESET_ALL+"token was: $"+thiscolor+f"{sim_total/(guage_bal/10**18):.0f}"+Style.RESET_ALL+") Simula: ["+Fore.CYAN+Style.BRIGHT+f"{100*((sim_total/_all_dollars_spent)-1):6.2f}"+Style.RESET_ALL+"%]")
        else:
            print("["+Fore.BLUE+f"{100*((sim_total/_all_dollars_spent)-1):5.2f}"+Style.RESET_ALL+"%]",end=' ')

        return sim_total

    except Exception:
        print("\nupdate tripool exception")
        return 0

if __name__ == "__main__":
    print(tri_calc(True,0))

    print(tri_calc(False,0))
