#!/usr/bin/env python3
"""convex functions"""
# pylint: disable=C0103,C0116,C0301,W0105,E0401,R0914
from web3 import Web3
from colorama import Fore, Style
from load_contract import load_contract

MY_WALLET_ADDRESS = "0x8D82Fef0d77d79e5231AE7BFcFeBA2bAcF127E2B"
INFURA_ID = "6aa1a043a9854eaa9fa68d17f619f326"
infura_w3 = Web3(Web3.HTTPProvider('https://mainnet.infura.io/v3/'+INFURA_ID))

cvx_3pool = load_contract("0x7091dbb7fcbA54569eF1387Ac89Eb2a5C9F6d2EA",infura_w3)#convex staking 3pool rewards
cvx_crv = load_contract("0x3Fe65692bfCD0e6CF84cB1E7d24108E434A7587e",infura_w3)#convex staking crv rewards
#cvx_token = load_contract("0x4e3FBD56CD56c3e72c1403e103b45Db9da5B9D2B",infura_w3)#cvx token to calculate ratio, cliff etc
#https://docs.convexfinance.com/convexfinanceintegration/cvx-minting
trix_crv = load_contract("0x5Edced358e6C0B435D53CC30fbE6f5f0833F404F",infura_w3)#convex tripool crv rewards

def convex_header_display(myarray, carray, w3, fullheader):

    print("xTripool"," "*16,(myarray[-1]["trix_rewards"][0]*carray["token_value_modifyer"][0]),end=" ")
    #print(Style.DIM+Fore.CYAN+str(format(round(myarray[-1][carray["name"][i]+"pool"]-(round(carray["minted"][i]/10**18,2)), 2), '.2f')).rjust(cw[3])+Style.RESET_ALL, end=' ')
    print(" "*23,Style.DIM+Fore.CYAN+str(round((myarray[-1]["trix_rewards"][2]*(myarray[-1]["USDcvx"]/myarray[-1]["USD"]))+myarray[-1]["trix_rewards"][1],2)),Style.RESET_ALL,end=" ")
    print(" "*9,"v"+str(format(round(myarray[-1]["trix_rewards"][1],2), '.2f')).rjust(5)+"x"+str(format(round(myarray[-1]["trix_rewards"][2],2), '.2f')).rjust(5),end="")

    myval = round((myarray[-1]["trix_rewards"][2]*myarray[-1]["USDcvx"])+
                  (myarray[-1]["trix_rewards"][1]*myarray[-1]["USD"]),2)

    print(" "*15,"$"+str(myval))

    print("xCRV"," "*27,"cvxCRV minted","Ç"+str(myarray[-1]["cvx_rewards"][0]),end=" ")
    print(" "*2,Style.DIM+Fore.CYAN+str(format(round((myarray[-1]["cvx_rewards"][3]*(myarray[-1]["USD3pool"]/myarray[-1]["USD"]))+(myarray[-1]["cvx_rewards"][2]*(myarray[-1]["USDcvx"]/myarray[-1]["USD"]))+myarray[-1]["cvx_rewards"][1],2), '.2f')),Style.RESET_ALL,end=" ")
    print(" "*9,"v"+str(format(round(myarray[-1]["cvx_rewards"][1],2), '.2f')).rjust(5)+"x"+str(format(round(myarray[-1]["cvx_rewards"][2],2), '.2f')).rjust(5)+"t"+str(format(round(myarray[-1]["cvx_rewards"][3],2), '.2f')).rjust(5),end="")

    myval = round((myarray[-1]["cvx_rewards"][3]*myarray[-1]["USD3pool"])+
                  (myarray[-1]["cvx_rewards"][2]*myarray[-1]["USDcvx"])+
                  (myarray[-1]["cvx_rewards"][1]*myarray[-1]["USD"]),2)

    print(" "*9,"$"+str(myval))

def cvx_getvalue(printit, myarray):
    try:
        invested = round(cvx_3pool.balanceOf(MY_WALLET_ADDRESS).call()/10**18)
        result = cvx_3pool.earned(MY_WALLET_ADDRESS).call()/10**18
        result2 = cvx_crv.earned(MY_WALLET_ADDRESS).call()/10**18
        CVX_fraction_factor = 0.4425 #HACK
        result3 = result2 * CVX_fraction_factor
        if printit:
            print(f"  CRV: {result2}")
            print(f"  CVX: {result3}")
            print(f"3pool: {result}")
        return [invested, result2, result3, result]
    except Exception:
        return [myarray[-1]["cvx_rewards"][0],myarray[-1]["cvx_rewards"][1],myarray[-1]["cvx_rewards"][2],myarray[-1]["cvx_rewards"][3]]

def trix_getvalue(printit, myarray):
    try:
        invested = round(trix_crv.balanceOf(MY_WALLET_ADDRESS).call()/10**18)
        result2 = trix_crv.earned(MY_WALLET_ADDRESS).call()/10**18
        CVX_fraction_factor = 0.4425 #HACK
        result3 = result2 * CVX_fraction_factor
        if printit:
            print(f"  CRV: {result2}")
            print(f"  CVX: {result3}")
        return [invested, result2, result3]
    except Exception:
        return [myarray[-1]["trix_rewards"][0],myarray[-1]["trix_rewards"][1],myarray[-1]["trix_rewards"][2]]

if __name__ == "__main__":
    a = cvx_getvalue(True, None)
    print(a,"\n\n")
    a = trix_getvalue(True, None)
    print(a)
