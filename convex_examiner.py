#!/usr/bin/env python3
"""convex functions"""
# pylint: disable=C0103,C0116,C0301,W0105,E0401,R0914
from web3 import Web3
from colorama import Fore, Style
from tools.load_contract import load_contract

CVX_fraction_factor = 0.37 #HACK

MY_WALLET_ADDRESS = "0x8D82Fef0d77d79e5231AE7BFcFeBA2bAcF127E2B"
#cvx_token = load_contract("0x4e3FBD56CD56c3e72c1403e103b45Db9da5B9D2B",infura_w3)#cvx token to calculate ratio, cliff etc
#https://docs.convexfinance.com/convexfinanceintegration/cvx-minting

def convex_header_display(myarray, carray):

    trix_value = ((myarray[-1]["trix_rewards"][2]*myarray[-1]["USDcvx"])+
                  (myarray[-1]["trix_rewards"][1]*myarray[-1]["USD"]))

    cvx_value = ((myarray[-1]["cvx_rewards"][3]*myarray[-1]["USD3pool"])+
                 (myarray[-1]["cvx_rewards"][2]*myarray[-1]["USDcvx"])+
                 (myarray[-1]["cvx_rewards"][1]*myarray[-1]["USD"]))

    cvxcrv_value = (myarray[-1]["cvxcrv_rewards"][1]*myarray[-1]["USDcvxCRV"])

    cvxsushi_value = (myarray[-1]["cvxsushi_rewards"][1]*myarray[-1]["USDcvx"])


    print("xTripool"," "*19,str((myarray[-1]["trix_rewards"][0]*carray["token_value_modifyer"][carray["longname"].index("tRicrypto")])).rjust(5),end=" ")
    print(" "*22,Style.DIM+Fore.CYAN+str(format(round((myarray[-1]["trix_rewards"][2]*(myarray[-1]["USDcvx"]/myarray[-1]["USD"]))+myarray[-1]["trix_rewards"][1],2),'5.2f')).rjust(6),Style.RESET_ALL,end=" ")
    print(" "*20,"$"+str(format(round(trix_value,2), '5.2f')).rjust(6),end=" ")
    print(" "*3,"v"+str(format(round(myarray[-1]["trix_rewards"][1],2), '5.2f')).rjust(5)+"x"+str(format(round(myarray[-1]["trix_rewards"][2],2), '5.2f')).rjust(5))

    print("Staked CRV"," "*17,Style.DIM+str(round(myarray[-1]["cvx_rewards"][0]*myarray[-1]["USDcvxCRV"])).rjust(5)+Style.RESET_ALL,end=" ")
    print(" "*8,"vv"+str(myarray[-1]["cvx_rewards"][0]),end=" ")
    print(" "*6,Style.DIM+Fore.CYAN+str(format(round((myarray[-1]["cvx_rewards"][3]*(myarray[-1]["USD3pool"]/myarray[-1]["USD"]))+(myarray[-1]["cvx_rewards"][2]*(myarray[-1]["USDcvx"]/myarray[-1]["USD"]))+myarray[-1]["cvx_rewards"][1],2), '5.2f')).rjust(6),Style.RESET_ALL,end=" ")
    print(" "*20,"$"+str(format(round(cvx_value,2), '5.2f')).rjust(6),end="")
    print(" "*37,"v"+str(format(round(myarray[-1]["cvx_rewards"][1],2), '5.2f')).rjust(5)+"x"+str(format(round(myarray[-1]["cvx_rewards"][2],2), '5.2f')).rjust(5)+"t"+str(format(round(myarray[-1]["cvx_rewards"][3],2), '5.2f')).rjust(5))

    print("Staked CVX"," "*17,Style.DIM+str(round(myarray[-1]["cvxcrv_rewards"][0]*myarray[-1]["USDcvx"])).rjust(5)+Style.RESET_ALL,end=" ")
    print(" "*9,"x"+str(round(myarray[-1]["cvxcrv_rewards"][0])).rjust(4),end=" ")
    print(" "*6,Style.DIM+Fore.CYAN+str(format(round(myarray[-1]["cvxcrv_rewards"][1]*(myarray[-1]["USDcvxCRV"]/myarray[-1]["USD"]),2),'5.2f')).rjust(6)+Style.RESET_ALL,end=" ")
    print(" "*21,"$"+str(format(round(cvxcrv_value,2), '5.2f')).rjust(6),end="")
    print(" "*68,"vv"+str(format(round(myarray[-1]["cvxcrv_rewards"][1],2), '5.2f')).rjust(5))

    cvxsushi_token_modifyer = 270 # HACK
    print("Sushi CVX/ETH"," "*14,Style.DIM+str(round(myarray[-1]["cvxsushi_rewards"][0]*cvxsushi_token_modifyer)).rjust(5)+Style.RESET_ALL,end=" ")
    print(" "*22,Style.DIM+Fore.CYAN+str(format(round(myarray[-1]["cvxsushi_rewards"][1]*(myarray[-1]["USDcvx"]/myarray[-1]["USD"]),2),'5.2f')).rjust(6)+Style.RESET_ALL,end=" ")
    print(" "*21,"$"+str(format(round(cvxsushi_value,2), '5.2f')).rjust(6),end="")
    print(" "*79,"x"+str(format(round(myarray[-1]["cvxsushi_rewards"][1],2), '5.2f')).rjust(5))


def cvx_getvalue(printit, myarray, w3):
    cvxcrv_3pool = load_contract("0x7091dbb7fcbA54569eF1387Ac89Eb2a5C9F6d2EA",w3)#convexCRV staking 3pool rewards
    cvxcrv_crv = load_contract("0x3Fe65692bfCD0e6CF84cB1E7d24108E434A7587e",w3)#convexCRV staking crv rewards
    try:
        invested = round(cvxcrv_3pool.balanceOf(MY_WALLET_ADDRESS).call()/10**18)
        tpool_earned = cvxcrv_3pool.earned(MY_WALLET_ADDRESS).call()/10**18
        crv_earned = cvxcrv_crv.earned(MY_WALLET_ADDRESS).call()/10**18
        cvx_earned = crv_earned * CVX_fraction_factor
        if printit:
            print(f"  CRV: {crv_earned}")
            print(f"  CVX: {cvx_earned}")
            print(f"3pool: {tpool_earned}")
        return [invested, crv_earned, cvx_earned, tpool_earned]
    except Exception:
        print("\nupdate cvx exception")
        return [myarray[-1]["cvx_rewards"][0],myarray[-1]["cvx_rewards"][1],myarray[-1]["cvx_rewards"][2],myarray[-1]["cvx_rewards"][3]]

def trix_getvalue(printit, myarray, w3):
    trix_crv = load_contract("0x9D5C5E364D81DaB193b72db9E9BE9D8ee669B652",w3)#convex tripool crv rewards
    try:
        invested = round(trix_crv.balanceOf(MY_WALLET_ADDRESS).call()/10**18)
        crv_earned = trix_crv.earned(MY_WALLET_ADDRESS).call()/10**18
        cvx_earned = crv_earned * CVX_fraction_factor
        if printit:
            print(f"  CRV: {crv_earned}")
            print(f"  CVX: {cvx_earned}")
        return [invested, crv_earned, cvx_earned]
    except Exception:
        print("\nupdate trix exception")
        return [myarray[-1]["trix_rewards"][0],myarray[-1]["trix_rewards"][1],myarray[-1]["trix_rewards"][2]]

def cvxcrv_getvalue(printit, myarray, w3):
    cvx_cvxcrv = load_contract("0xCF50b810E57Ac33B91dCF525C6ddd9881B139332",w3)#convex cvxCRV rewards
    try:
        invested = cvx_cvxcrv.balanceOf(MY_WALLET_ADDRESS).call()/10**18
        cvxcrv_earned = cvx_cvxcrv.earned(MY_WALLET_ADDRESS).call()/10**18
        if printit:
            print(f"  cvxCRV: {cvxcrv_earned}")
        return [invested, cvxcrv_earned]
    except Exception:
        print("\nupdate cvxcrv exception")
        return [myarray[-1]["cvxcrv_rewards"][0] ,myarray[-1]["cvxcrv_rewards"][1]]

def cvxsushi_getvalue(printit, myarray, w3):
    sushi=load_contract("0xEF0881eC094552b2e128Cf945EF17a6752B4Ec5d", w3)
    cvx_rewarder=load_contract("0x9e01aaC4b3e8781a85b21d9d9F848e72Af77B362", w3)
    try:
        invested = cvx_rewarder.sushiBalanceOf(MY_WALLET_ADDRESS).call()/10**18
        cvx_earned = cvx_rewarder.earned(MY_WALLET_ADDRESS).call()/10**18
        sushi_earned = sushi.pendingSushi(1,MY_WALLET_ADDRESS).call()/10**18
        if printit:
            print(f"  cvx/eth sushi pool cvx: {cvx_earned}")
            print(f"  cvx/eth sushi pool sushi: {sushi_earned}")
        return [invested, cvx_earned, sushi_earned]
    except Exception:
        print("\nupdate cvx/eth sushi exception")
        return [myarray[-1]["cvxsushi_rewards"][0], myarray[-1]["cvxsushi_rewards"][1], myarray[-1]["cvxsushi_rewards"][2]]

if __name__ == "__main__":
    INFURA_ID = "1d651358519346beb661128bf65ab651"
    infura_w3 = Web3(Web3.HTTPProvider('https://mainnet.infura.io/v3/'+INFURA_ID))
    a = cvx_getvalue(True, None, infura_w3)
    print(a,"\n\n")
    a = trix_getvalue(True, None, infura_w3)
    print(a,"\n\n")
    a = cvxcrv_getvalue(True, None, infura_w3)
    print(a,"\n\n")
    a = cvxsushi_getvalue(True, None, infura_w3)
    print(a)
