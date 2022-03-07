#!/usr/bin/env python3
"""convex functions"""
# pylint: disable=C0103,C0116,C0301,W0105,E0401,R0914
from web3 import Web3
from tools.load_contract import load_contract

CVX_fraction_factor = [0.148,.3155] #HACK

MY_WALLET_ADDRESS = "0x8D82Fef0d77d79e5231AE7BFcFeBA2bAcF127E2B"
#cvx_token = load_contract("0x4e3FBD56CD56c3e72c1403e103b45Db9da5B9D2B",infura_w3)#cvx token to calculate ratio, cliff etc
#https://docs.convexfinance.com/convexfinanceintegration/cvx-minting

def cvx_getvalue(myarray, w3, printit=0):
    cvxcrv_3pool = load_contract("0x7091dbb7fcbA54569eF1387Ac89Eb2a5C9F6d2EA",w3)#convexCRV staking 3pool rewards
    cvxcrv_crv = load_contract("0x3Fe65692bfCD0e6CF84cB1E7d24108E434A7587e",w3)#convexCRV staking crv rewards
    try:
        invested = round(cvxcrv_3pool.balanceOf(MY_WALLET_ADDRESS).call()/10**18)
        tpool_earned = cvxcrv_3pool.earned(MY_WALLET_ADDRESS).call()/10**18
        crv_earned = cvxcrv_crv.earned(MY_WALLET_ADDRESS).call()/10**18
        cvx_earned = crv_earned * CVX_fraction_factor[0]
        if printit:
            print(f"  CRV: {crv_earned}")
            print(f"  CVX: {cvx_earned}")
            print(f"3pool: {tpool_earned}")
        return [invested, crv_earned, cvx_earned, tpool_earned]
    except Exception:
        print("\nupdate cvx exception")
        return [myarray[-1]["cvx_rewards"][0],myarray[-1]["cvx_rewards"][1],myarray[-1]["cvx_rewards"][2],myarray[-1]["cvx_rewards"][3]]

def regx_getvalue(myarray, w3, fallback, pool_id, which_factor=0, printit=0):
    regx_crv = load_contract(pool_id, w3)#convex tripool crv rewards
    try:
        invested = regx_crv.balanceOf(MY_WALLET_ADDRESS).call()/10**18
        crv_earned = regx_crv.earned(MY_WALLET_ADDRESS).call()/10**18
        cvx_earned = crv_earned * CVX_fraction_factor[which_factor]
        if printit:
            print(f"  CRV: {crv_earned}")
            print(f"  CVX: {cvx_earned}")
        return [invested, crv_earned, cvx_earned]
    except Exception:
        print("\nupdate regx exception")
        return [myarray[-1][fallback][0],myarray[-1][fallback][1],myarray[-1][fallback][2]]

def cvxcrv_getvalue(myarray, w3, printit=0):
    cvx_cvxcrv = load_contract("0x72a19342e8F1838460eBFCCEf09F6585e32db86E", w3)#convex cvxCRV rewards
    try:
        invested = cvx_cvxcrv.balances(MY_WALLET_ADDRESS).call()[0]/10**18
        cvxcrv_earned=cvx_cvxcrv.claimableRewards(MY_WALLET_ADDRESS).call()[0][1]/10**18
        if printit:
            print(f"  cvxCRV: {cvxcrv_earned}")
        return [invested, cvxcrv_earned]
    except Exception:
        print("\nupdate cvxcrv exception")
        if not printit:
            return [myarray[-1]["cvxcrv_rewards"][0], myarray[-1]["cvxcrv_rewards"][1]]

def cvxsushi_getvalue(myarray, w3, printit=0):
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

def virt_grabber(myarray, w3, fallback, pool_id, printit=0):  
    crveth_token = load_contract(pool_id,w3)
    try:
        virt = crveth_token.get_virtual_price().call()/10**18
        if printit:
            print(virt)
        else:
            if virt >= myarray[-1][fallback]:
                return virt
            else:
                #return virt
                return myarray[-1][fallback]
    except:
        print("\nupdate virt exception")
        return myarray[-1][fallback]

def earned_grabber(myarray, w3, fallback, pool_id, printit=0):
    try:
        return load_contract(pool_id,w3).earned(MY_WALLET_ADDRESS).call()/10**18
    except:
        print("\nupdate balance exception")
        #return myarray[-1][fallback]

if __name__ == "__main__":
    INFURA_ID = "1d651358519346beb661128bf65ab651"
    infura_w3 = Web3(Web3.HTTPProvider('https://mainnet.infura.io/v3/'+INFURA_ID))
    a = cvx_getvalue(None, infura_w3, True)
    print(a,"\n\n")
    a = regx_getvalue(None, infura_w3, "trix_rewards", "0x9D5C5E364D81DaB193b72db9E9BE9D8ee669B652", True)
    print(a,"\n\n")
    a = regx_getvalue(None, infura_w3, "mimx_rewards", "0xC62DE533ea77D46f3172516aB6b1000dAf577E89", True)
    print(a,"\n\n")
    a = regx_getvalue(None, infura_w3, "crveth_rewards", "0x085A2054c51eA5c91dbF7f90d65e728c0f2A270f", True)
    print(a,"\n\n")
    a = regx_getvalue(None, infura_w3, "cvxeth_rewards", "0xb1Fb0BA0676A1fFA83882c7F4805408bA232C1fA",1, True)
    print(a,"\n\n")
    a = regx_getvalue(None, infura_w3, "spelleth_rewards", "0xb2f0bB6352417c1Bf017862aC165E67623611aF3", True)
    print(a,"\n\n")
    a = regx_getvalue(None, infura_w3, "cvxfxs_rewards", "0xf27AFAD0142393e4b3E5510aBc5fe3743Ad669Cb", True)
    print(a,"\n\n")
    a = cvxcrv_getvalue(None, infura_w3, True)
    print(a,"\n\n")
    a = cvxsushi_getvalue(None, infura_w3, True)
    print(a)
    a = virt_grabber(None, infura_w3, "crveth_virt", "0x8301AE4fc9c624d1D396cbDAa1ed877821D7C511", True)
    a = virt_grabber(None, infura_w3, "cvxeth_virt", "0xB576491F1E6e5E62f1d8F26062Ee822B40B0E0d4", True)
    a = virt_grabber(None, infura_w3, "spelleth_virt", "0x98638FAcf9a3865cd033F36548713183f6996122", True)
    a = virt_grabber(None, infura_w3, "cvxfxs_virt", "0xd658A338613198204DCa1143Ac3F01A722b5d94A", True)
    a = earned_grabber(None, infura_w3,"cvxfxs_extracvx ","0xE2585F27bf5aaB7756f626D6444eD5Fc9154e606", True)
    print(a)
    a = earned_grabber(None, infura_w3,"cvxfxs_extrafxs","0x28120D9D49dBAeb5E34D6B809b842684C482EF27", True)    
    print(a)
    a = earned_grabber(None, infura_w3,"cvxeth_extracvx","0x834B9147Fd23bF131644aBC6e557Daf99C5cDa15", True)    
    print(a)
    a = regx_getvalue(None, infura_w3, "cvxeth_rewards", "0xb1Fb0BA0676A1fFA83882c7F4805408bA232C1fA",0, True)
    print(a,"\n\n")