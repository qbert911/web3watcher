#!/usr/bin/env python3
"""tripool functions"""
# pylint: disable=C0103,C0116,C0301,W0105,E0401,R0914
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

tri_gauge = load_contract("0xDeFd8FdD20e0f34115C7018CCfb655796F6B2168",infura_w3)
tri_swap = load_contract("0xD51a44d3FaE010294C616388b506AcdA1bfAAE46",infura_w3)

def tri_calc(fulldisplay):
    sim_total = 0
    _price_oracle = [1,0,0]
    try:
        _coins_in_convex_gauge = convex_examiner.regx_getvalue(False,None,infura_w3,"trix_rewards","0x9D5C5E364D81DaB193b72db9E9BE9D8ee669B652")[0]
        gauge_bal = tri_gauge.balanceOf(MY_WALLET_ADDRESS).call() + (_coins_in_convex_gauge*(10**18))
        _all_dollars_spent = sum(item['dollar_value'] for item in purchase_array) * ((gauge_bal/10**18)/sum(item['tokens_recieved'] for item in purchase_array))
        virt_price = tri_swap.get_virtual_price().call()/10**18
        _price_oracle[1] = tri_swap.price_oracle(0).call()/10**18
        _price_oracle[2] = tri_swap.price_oracle(1).call()/10**18
        calculated_token_value = 3 * virt_price * ((_price_oracle[2] * _price_oracle[1])**(1/3))
        estimated_total = round(gauge_bal*calculated_token_value/10**18)
        if fulldisplay:
            print(f"   virtprice: {virt_price}\n"+f" Tokens held: {gauge_bal / 10 ** 18:.4f}\n")

        for j in range(len(purchase_array)):
            x = _price_oracle[1] / purchase_array[j]["btc_price"]
            y = _price_oracle[2] / purchase_array[j]["eth_price"]
            z = (x+y+1) / 3
            sim_total += z * purchase_array[j]['dollar_value'] * ((gauge_bal/10**18)/sum(item['tokens_recieved'] for item in purchase_array))
            if fulldisplay:
                thiscolor = Fore.RED+Style.BRIGHT
                if _all_dollars_spent < sim_total:
                    thiscolor = Fore.GREEN+Style.BRIGHT
                print(f"Purchase #{j+1: 2d}: $"+Fore.GREEN+f"{purchase_array[j]['dollar_value']:06,d}"+Style.RESET_ALL, end = "")
                print("  for  ©"+Fore.MAGENTA+f"{purchase_array[j]['tokens_recieved']:5.2f}"+Style.RESET_ALL+f"      ${purchase_array[j]['dollar_value']/purchase_array[j]['tokens_recieved']:.0f}", end = "   ")
                print("Sim ["+Fore.CYAN+Style.BRIGHT+f"{(z-1)*100:6.2f}"+Style.RESET_ALL+"%] "+f"BTC[{(x-1) * 100:6.2f}%] ETH[{(y-1) * 100:6.2f}%]")
        if fulldisplay:
            print(" "*3,"Invested: $"+Fore.GREEN+f"{_all_dollars_spent:,.0f}"+Style.RESET_ALL+" (Each "+Fore.MAGENTA+"©"+Style.RESET_ALL+f"token was: ${_all_dollars_spent/(gauge_bal/10**18):.0f}) \n")
            print(" "*2,"Simulated: $"+Fore.YELLOW+f"{sim_total:,.0f}"+Style.RESET_ALL+" (Each "+Fore.MAGENTA+"©"+Style.RESET_ALL+"token was: $"+thiscolor+f"{sim_total/(gauge_bal/10**18):.0f}"+Style.RESET_ALL+") Simula: ["+Fore.CYAN+Style.BRIGHT+f"{100*((sim_total/_all_dollars_spent)-1):6.2f}"+Style.RESET_ALL+"%]\n")
            print(" "*2,"Estimated: $"+f"{estimated_total:,.0f}",end='')
            print(" (Each "+Fore.MAGENTA+"©"+Style.RESET_ALL+"token was: $"+thiscolor+f"{estimated_total/(gauge_bal/10**18):.0f}"+Style.RESET_ALL+") Simula: ["+Fore.CYAN+Style.BRIGHT+f"{100*((estimated_total/_all_dollars_spent)-1):6.2f}"+Style.RESET_ALL+"%]\n")
        if sim_total > estimated_total:  #use the lower of the two estimates for other calculations
            sim_total = estimated_total
        return (sim_total/_all_dollars_spent), "["+Fore.BLUE+f"{100*((sim_total/_all_dollars_spent)-1):5.2f}"+Style.RESET_ALL+"%]"

    except Exception:
        print("\nupdate tripool exception")
        return 0

if __name__ == "__main__":
    print(tri_calc(True))
    print(tri_calc(False))
    #token_price = round(load_contract("0xE8b2989276E2Ca8FDEA2268E3551b2b4B2418950",infura_w3).lp_price().call() / 10 ** 18)
    #print(token_price)
