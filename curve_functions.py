#!/usr/bin/env python3
"""curve"""
# pylint: disable=C0103,C0301,W0105,E0401,R0914,C0411,W0702,C0200,C0116,w0106
import time
import json
from colorama import Fore, Style
from tools.load_contract import load_contract

MY_WALLET_ADDRESS = "0x8D82Fef0d77d79e5231AE7BFcFeBA2bAcF127E2B"

def call_me(function,expecting_list=False):
    """input filtering"""
    x = function.call()
    if isinstance(x, list):
        if not expecting_list:
            print("\n unexpected list found when calling: ",function,x)
        x = x[0]
    if 0 < x < 10000:
        print("\n odd output when calling "+str(function),x)
    return x

def load_curvepools_fromjson(myarray,barray,w3):
    """prepare iteratable array from json file"""
    with open("curvepools.json", 'r') as thisfile:
        thisarray = json.load(thisfile)
    minter_func = load_contract("0xd061D61a4d941c39E5453435B6345Dc261C2fcE0",w3)

    barray["minted"] = [0]*len(thisarray)
    barray["balanceof"] = [0]*len(thisarray)
    barray["raw"] = [0]*len(thisarray)
    barray["totalsupply"] = [0]*len(thisarray)
    barray["futureboost"] = [0]*len(thisarray)
    barray["booststatus"] = [0]*len(thisarray)
    barray["virtprice"] = [0]*len(thisarray)
    barray["token_value_modifyer"] = [0]*len(thisarray)
    print(len(thisarray),"pools loaded from curvepools.json")
    for i in range(len(thisarray)):
        barray["longname"].append(thisarray[i]["longname"])
        barray["invested"].append(thisarray[i]["invested"])
        barray["currentboost"].append(thisarray[i]["currentboost"])
        barray["name"].append(thisarray[i]["name"])
        barray["gaugeaddress"].append(thisarray[i]["gaugeaddress"])
        barray["swapaddress"].append(thisarray[i]["swapaddress"])
        try:
            barray["minted"][i] = call_me(minter_func.minted(MY_WALLET_ADDRESS, barray["gaugeaddress"][i]))
            barray["tokenaddress"].append(thisarray[i]["tokenaddress"])
        except Exception:
            barray["tokenaddress"].append("")
        #try:
        #    _ = myarray[-1][barray["name"][i]+"pool"]
        #except Exception:
           # print(thisarray[i]["longname"], "not found in current history file, adding now.")
           #myarray[-1][barray["name"][i]+"pool"] = 0
            #myarray[-1][barray["name"][i]+"invested"] = 0
        try:
            barray["token_value_modifyer"][i] = thisarray[i]["token_value_modifyer"]
        except Exception:
            barray["token_value_modifyer"][i] = 1

def update_curve_pools(mydict,carray,myarray,myarrayh,w3):
    minter_func = load_contract("0xd061D61a4d941c39E5453435B6345Dc261C2fcE0",w3)
    for i in range(len(carray["name"])):
        if carray["invested"][i] > 0:
            mydict[carray["name"][i]+"invested"] = carray["invested"][i]
            try:
                if carray["invested"][i] > 0: #skip updating empty pools
                    carray["balanceof"][i] = call_me(load_contract(carray["gaugeaddress"][i],w3).balanceOf(MY_WALLET_ADDRESS))/10**18
                    time.sleep(0.1)
                    carray["raw"][i] = call_me(load_contract(carray["gaugeaddress"][i],w3).claimable_tokens(MY_WALLET_ADDRESS))
                    potential_virtprice_update = call_me(load_contract(carray["swapaddress"][i],w3).get_virtual_price())/10**18
                    if potential_virtprice_update > carray["virtprice"][i]:
                        carray["virtprice"][i] = potential_virtprice_update
                        mydict[carray["name"][i]+"virtprice"] = potential_virtprice_update
                    else:
                        mydict[carray["name"][i]+"virtprice"] = carray["virtprice"][i]
                    if (carray["virtprice"][i]*carray["balanceof"][i]*carray["token_value_modifyer"][i])-carray["invested"][i] > -10:
                        mydict[carray["name"][i]+"profit"] = (carray["virtprice"][i]*carray["balanceof"][i]*carray["token_value_modifyer"][i])-carray["invested"][i]
                if abs(round((carray["raw"][i]+carray["minted"][i])/10**18, 5) - myarray[-1][carray["name"][i]+"pool"]) > 10:
                    print("\nMINTING HAPPENED:", carray["name"][i], "pool      Before", carray["minted"][i], end='   ')
                    carray["minted"][i] = call_me(minter_func.minted(MY_WALLET_ADDRESS, carray["gaugeaddress"][i]))
                    print("After", carray["minted"][i])
                mydict[carray["name"][i]+"pool"] = round((carray["raw"][i]+carray["minted"][i])/10**18, 5)
                if myarray[-1][carray["name"][i]+"pool"] - mydict[carray["name"][i]+"pool"] > 0.01: #debug lines ... should not happen
                    print(myarray[-1][carray["name"][i]+"pool"] - mydict[carray["name"][i]+"pool"], "\nerror with lower raw value"+carray["name"][i], myarray[-1][carray["name"][i]+"pool"], mydict[carray["name"][i]+"pool"], end='')
            except Exception: #usually happens when snx is down for maintenance
                print("\nupdate curve pools exception", carray["name"][i], i)
                time.sleep(1)
                mydict[carray["name"][i]+"pool"] = myarrayh[-1][carray["name"][i]+"pool"]
                carray["raw"][i] = (myarrayh[-1][carray["name"][i]+"pool"]*10**18) - carray["minted"][i]
    mydict["claim"] = round((sum(carray["raw"])+sum(carray["minted"]))/10**18, 6)

def curve_boost_check(carray,w3):
    """update variables to check boost status"""
    print('[', end='')
    try:
        vecrv_func = load_contract("0x5f3b5DfEb7B28CDbD7FAba78963EE202a494e2A2",w3)
        veCRV_mine = round(call_me(vecrv_func.balanceOf(MY_WALLET_ADDRESS))/10**18, 2)
        veCRV_total = round(call_me(vecrv_func.totalSupply())/10**18, 2)
        outputflag = 0
        for i in range(len(carray["name"])):
            if carray["currentboost"][i] >= 2.47:   #hack to avoid spool which is annoyingly close to 2.5 boost
                carray["booststatus"][i] = -1               #Green, all is well
            elif carray["currentboost"][i] == 0:
                carray["booststatus"][i] = 4                #Blue, pool is empty
            else:
                carray["balanceof"][i] = round(call_me(load_contract(carray["gaugeaddress"][i],w3).balanceOf(MY_WALLET_ADDRESS))/10**18, 2)
                carray["totalsupply"][i] = round(call_me(load_contract(carray["gaugeaddress"][i],w3).totalSupply())/10**18, 2)
                if carray["currentboost"][i] > 0:
                    carray["futureboost"][i] = 2.5 * min((carray["balanceof"][i]/2.5) + (carray["totalsupply"][i]*veCRV_mine/veCRV_total*(1-(1/2.5))), carray["balanceof"][i])/carray["balanceof"][i]
                if carray["currentboost"][i] >= carray["futureboost"][i]:
                    carray["booststatus"][i] = 1            #Gray, boost status was higher before, nothing to do
                else:
                    outputflag = 1
                    print(carray["name"][i], end='')
                    if carray["futureboost"][i]-carray["currentboost"][i] >= .05:
                        carray["booststatus"][i] = 2        #Red, big enough change in boost status to care
                        print(Style.BRIGHT+Fore.RED+str(format(round((carray["futureboost"][i]-carray["currentboost"][i])*10000), '04')).rjust(4)+Style.RESET_ALL, end=' ')
                    else:
                        carray["booststatus"][i] = 3        #Purple, small change in boost status
                        print(Style.DIM+Fore.RED+str(format(round((carray["futureboost"][i]-carray["currentboost"][i])*10000), '04')).rjust(4)+Style.RESET_ALL, end=' ')

        if not outputflag:
            print(f'{Fore.GREEN}Bööst{Style.RESET_ALL}', end=' ')
    except Exception:
        print("uperr", end=' ')
    print('\b] ', end='')    

if __name__ == "__main__":
    print("this module is not meant to be run solo")
