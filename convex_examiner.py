#!/usr/bin/env python3
"""convex functions"""
# pylint: disable=C0103,C0116,C0301,W0105,E0401,R0914
from web3 import Web3
from tools.load_contract import load_contract

CVX_fraction_factor = [0.042] #HACK

MY_WALLET_ADDRESS = "0x8D82Fef0d77d79e5231AE7BFcFeBA2bAcF127E2B"
#cvx_token = load_contract("0x4e3FBD56CD56c3e72c1403e103b45Db9da5B9D2B",infura_w3)#cvx token to calculate ratio, cliff etc
#https://docs.convexfinance.com/convexfinanceintegration/cvx-minting

def crvstaked_getvalue(myarray, w3, pool_id, printit=0):
    cvxcrv_crv = load_contract(pool_id,w3)#convexCRV staking crv rewards
    cvxcrv_3pool = load_contract("0x7091dbb7fcbA54569eF1387Ac89Eb2a5C9F6d2EA",w3)#convexCRV staking 3pool rewards
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
        print("\nupdate staked crv exception")
        return [myarray[-1]["crvstaked_rewards"][0],myarray[-1]["crvstaked_rewards"][1],myarray[-1]["crvstaked_rewards"][2],myarray[-1]["crvstaked_rewards"][3]]

def cvxlocked_getvalue(myarray, w3, pool_id, printit=0):
    cvx_locked = load_contract(pool_id, w3)#convex locked rewards
    try:
        invested = cvx_locked.balances(MY_WALLET_ADDRESS).call()[0]/10**18
        cvxlocked_earned=cvx_locked.claimableRewards(MY_WALLET_ADDRESS).call()[0][1]/10**18
        cvxlocked_earned2=cvx_locked.claimableRewards(MY_WALLET_ADDRESS).call()[1][1]/10**18
        if printit:
            print(f"  cvxlocked: {cvxlocked_earned}")
        return [invested, cvxlocked_earned, cvxlocked_earned2]
    except Exception:
        print("\nupdate cvxlocked exception")
        if not printit:
            return [myarray[-1]["cvxlocked_rewards"][0], myarray[-1]["cvxlocked_rewards"][1],myarray[-1]["cvxlocked_rewards"][2]]

def call_constant(constants, label, function):
    """input filtering"""
    if label in constants:
        x = constants[label]
        #print("found ",label,x)
    else:
        x = constants[label] = function.call()
        #print("adding",label,x)
    return x,constants

def regx_getvalue(myarray, w3, fallback, constants, printit=0, wallet_address = MY_WALLET_ADDRESS, poolid = 0):
    main_contract = load_contract("0xF403C135812408BFbE8713b5A23a04b3D48AAE31",w3)
    poolinfo_addresses_array, constants = call_constant(constants,f"p{poolid}",main_contract.poolInfo(poolid)) #load a single pools' addresses from the main convex contract
    regx_crv = load_contract(poolinfo_addresses_array[3], w3)#convex tripool crv rewards

    try:   
        minter, constants = call_constant(constants,f"minter{poolinfo_addresses_array[3]}", load_contract(poolinfo_addresses_array[0],w3, minter_abi=True).minter()) 
    except Exception:
        minter = poolinfo_addresses_array[0]

    virtprice = load_contract(minter,w3, lp_abi=True).get_virtual_price().call()/10**18
    if virtprice < myarray[-1][fallback][4]:
        virtprice = myarray[-1][fallback][4]

    try:
        invested = regx_crv.balanceOf(wallet_address).call()/10**18
        crv_earned = regx_crv.earned(wallet_address).call()/10**18
        cvx_earned = crv_earned * CVX_fraction_factor[0]
        extra_list = []
        num_extra_rewards, constants = call_constant(constants,f"erl  {poolinfo_addresses_array[3]}",regx_crv.extraRewardsLength())
        for i in range(num_extra_rewards):
            reward_contract, constants = call_constant(constants,f"er{i}  {poolinfo_addresses_array[3]}", regx_crv.extraRewards(i))
            reward_token, constants = call_constant(constants,f"er{i}t {poolinfo_addresses_array[3]}",load_contract(reward_contract, w3).rewardToken())
            token_name, constants = call_constant(constants,f"er{i}tn{poolinfo_addresses_array[3]}", load_contract(reward_token,w3).symbol())
            extra_dict = {'amount': load_contract(reward_contract, w3).earned(wallet_address).call() / 10**18,
                          'name' : token_name}
            extra_list.append(extra_dict)
        if printit:
            print(f"  CRV: {crv_earned}")
            print(f"  CVX: {cvx_earned}")
        return [invested, crv_earned, cvx_earned, extra_list, virtprice], constants
    except Exception:
        print("\nupdate regx exception")
        return myarray[-1][fallback], constants

def abracadabra_getvalue(myarray, w3, fallback, pool_id, constants, printit=0):
    try:
        abracadabra_contract = load_contract(pool_id, w3)
        tokens_owned = abracadabra_contract.userInfo(0,MY_WALLET_ADDRESS).call()[0]
        rewards_waiting = round(abracadabra_contract.pendingIce(0,MY_WALLET_ADDRESS).call()/10**18,2)
        
        slp_pool_contract, constants = call_constant(constants,f"a{pool_id}",abracadabra_contract.poolInfo(0))
        slp_pool=load_contract(slp_pool_contract[0], w3) 
        total_supply=slp_pool.totalSupply().call()
        reserves=slp_pool.getReserves().call()
        owned_spell = round((tokens_owned / total_supply ) * reserves[0]/10**18)
        owned_eth = round((tokens_owned / total_supply ) * reserves[1]/10**18,8)

        if printit:
            print(f"\n{round(tokens_owned/10**18,8)} sushi lp tokens owned")
            print(round(total_supply/10**18,8), "sushi lp tokens total\n")
            print(round(reserves[0]/10**18),"spell in total")
            print(round(reserves[1]/10**18),"eth in total\n")

            print(owned_spell,"spell owned")
            print(owned_eth,"eth owned\n")

        return [owned_eth, owned_spell, rewards_waiting], constants
    except Exception:
        print("abracadabra update error")
        return myarray[-1][fallback], constants

def stakedao_getvalue(myarray, w3, fallback, pool_id, printit=0):
    try:
        stakedao_contract = load_contract(pool_id, w3, stakedao_abi=True)
        tokens_owned = round(stakedao_contract.balanceOf(MY_WALLET_ADDRESS).call()/10**18,8)
        rewards_waiting1 = round(stakedao_contract.claimable_reward(MY_WALLET_ADDRESS,"0x73968b9a57c6E53d41345FD57a6E6ae27d6CDB2F").call()/10**18,8)
        rewards_waiting2 = round(stakedao_contract.claimable_reward(MY_WALLET_ADDRESS,"0x6c3F90f043a72FA612cbac8115EE7e52BDe6E490").call()/10**18,8)
        rewards_waiting3 = round(stakedao_contract.claimable_reward(MY_WALLET_ADDRESS,"0xD533a949740bb3306d119CC777fa900bA034cd52").call()/10**18,8)
        return [tokens_owned, rewards_waiting1, rewards_waiting2, rewards_waiting3]
    except Exception:
        print("stakedao update error")
        return myarray[-1][fallback]

def concentrator_getvalues(myarray, w3):

    try:        
        concentrator = load_contract("0x3Cf54F3A1969be9916DAD548f3C084331C4450b5",w3,"0x99373AE646ed89b9A466c4256b09b10dbCC07B40")
        concentrator_rewards_CTR = concentrator.pendingRewardAll(MY_WALLET_ADDRESS).call()/10**18
        concentrator_x2e_virt = concentrator.getTotalUnderlying(5).call() / concentrator.getTotalShare(5).call()

        acrv = load_contract("0x2b95A1Dcc3D405535f9ed33c219ab38E8d7e0884",w3,"0x160D6e417bE17E21712F004B87872a30799Cb78f")
        concentrator_virt = acrv.totalUnderlying().call() / acrv.totalSupply().call()
        
        ve_concentrator = load_contract("0xe4C09928d834cd58D233CD77B5af3545484B4968",w3)
        ve_current = ve_concentrator.balanceOf(MY_WALLET_ADDRESS).call()/10**18
        ve_locked = myarray[-1]["concentrator_ve_locked"] #ve_concentrator.locked(MY_WALLET_ADDRESS).call()[0]/10**18

        air_concentrator = load_contract("0x8341889905BdEF85b87cb7644A93F7a482F28742",w3)
        air_claimable = air_concentrator.vested(MY_WALLET_ADDRESS).call()/10**18
        air_locked = air_concentrator.locked(MY_WALLET_ADDRESS).call()/10**18

        return concentrator_rewards_CTR, concentrator_virt, concentrator_x2e_virt, ve_current, ve_locked, air_claimable, air_locked
    except Exception:
        print("\nconcentrator update error\n")
        return myarray[-1]["concentrator_rewards_CTR"], myarray[-1]["concentrator_virt"], myarray[-1]["concentrator_x2e_virt"],myarray[-1]["concentrator_ve_current"], myarray[-1]["concentrator_ve_locked"],\
               myarray[-1]["concentrator_air_claimable"], myarray[-1]["concentrator_air_locked"]

if __name__ == "__main__":
    INFURA_ID = "1d651358519346beb661128bf65ab651"
    infura_w3 = Web3(Web3.HTTPProvider(f'https://mainnet.infura.io/v3/{INFURA_ID}'))
    a = crvstaked_getvalue(None, infura_w3, "0x3Fe65692bfCD0e6CF84cB1E7d24108E434A7587e", True)
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
    a = regx_getvalue(None, infura_w3, "fxslocked_rewards", "0xf27AFAD0142393e4b3E5510aBc5fe3743Ad669Cb", True)
    print(a,"\n\n")
    a = cvxlocked_getvalue(None, infura_w3, "0x72a19342e8F1838460eBFCCEf09F6585e32db86E", True)
    print(a,"\n\n")
    a = regx_getvalue(None, infura_w3, "cvxeth_rewards", "0xb1Fb0BA0676A1fFA83882c7F4805408bA232C1fA",0, True)
    print(a,"\n\n")