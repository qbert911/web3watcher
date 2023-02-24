#!/usr/bin/env python3
from web3 import Web3
from load_contract import load_contract

MY_WALLET_ADDRESS = "0x8D82Fef0d77d79e5231AE7BFcFeBA2bAcF127E2B"
INFURA_ID = "1d651358519346beb661128bf65ab651"
infura_w3 = Web3(Web3.HTTPProvider(f'https://mainnet.infura.io/v3/{INFURA_ID}'))

def get_chainlink_price(contract_address, w3):
    contract = load_contract(contract_address, w3)
    return contract.latestAnswer().call() / 10**contract.decimals().call()

def abracadabra_getvalue(myarray, w3, fallback, pool_id, printit=0):
    try:
        abracadabra_contract = load_contract(pool_id, w3)
        tokens_owned = abracadabra_contract.userInfo(0,MY_WALLET_ADDRESS).call()[0]
        rewards_waiting = round(abracadabra_contract.pendingIce(0,MY_WALLET_ADDRESS).call()/10**18,2)
        
        slp_pool=load_contract(abracadabra_contract.poolInfo(0).call()[0], w3)
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

        return [owned_eth, owned_spell, rewards_waiting]
    except Exception:
        print("abracadabra update error")
        return myarray[-1][fallback]

def main():
    myarray =[]

    mydict = {"abra_spelleth": abracadabra_getvalue(myarray, infura_w3, "abra_spelleth", "0xF43480afE9863da4AcBD4419A47D9Cc7d25A647F",0)}
    SPELL = get_chainlink_price('0x8c110B94C5f1d347fAcF5E1E938AB2db60E3c9a8',infura_w3)
    ETH = get_chainlink_price('0x5f4eC3Df9cbd43714FE2740f5E3616155c5b8419',infura_w3)

    print(mydict["abra_spelleth"])
    print(f"{mydict['abra_spelleth'][1]*SPELL + mydict['abra_spelleth'][0]*ETH:.2f} stack worth")
    print(f"\n{mydict['abra_spelleth'][2]:.2f} Spell earned")
    print(f"{mydict['abra_spelleth'][2]*SPELL:.2f} Dollars earned")

    #crv staking wrapper testing
    contract = load_contract("0xaa0C3f5F7DFD688C6E646F66CD2a6B66ACdbE434", infura_w3)
    x=contract.earned(MY_WALLET_ADDRESS).call() 
    print(x)
    x=contract.balanceOf(MY_WALLET_ADDRESS).call() 
    print(x)

    #cnc staking testing
    contract = load_contract("0xC67e9Cdf599369130DD0841Ee5CB8eBF9BB661C4", infura_w3)
    x=contract.claimableRewards(MY_WALLET_ADDRESS).call() 
    print(x)
    x=contract.balances(MY_WALLET_ADDRESS).call() 
    print(x)
    x=contract.claimRewards().call() 
    print(x)

    #abccvx staking testing
    contract = load_contract("0xc5022291cA8281745d173bB855DCd34dda67F2f0", infura_w3)
    x=contract.claimable_tokens(MY_WALLET_ADDRESS).call() 
    print(x)
    x=contract.balanceOf(MY_WALLET_ADDRESS).call() 
    print(x)

    #ctr locked testing
    contract = load_contract("0xA5D9358c60fC9Bd2b508eDa17c78C67A43A4458C", infura_w3)
    x=contract.claim(MY_WALLET_ADDRESS).call() 
    print("\n",x)


if __name__ == "__main__":
    main()