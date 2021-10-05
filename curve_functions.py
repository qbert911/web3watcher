#!/usr/bin/env python3
"""curve"""
# pylint: disable=C0103,C0301,W0105,E0401,R0914,C0411,W0702,C0200,C0116,w0106
import json
import time
from colorama import Fore, Style
from tools.load_contract import load_contract, call_me

MY_WALLET_ADDRESS = "0x8D82Fef0d77d79e5231AE7BFcFeBA2bAcF127E2B"
csym = Fore.MAGENTA + Style.BRIGHT + "Ç" + Style.RESET_ALL + Fore.CYAN

def curve_header_display(myarray, carray, w3, fullheader):
    """display detailed pool information"""
    vecrv_func = load_contract("0x5f3b5DfEb7B28CDbD7FAba78963EE202a494e2A2",w3)
    virutal_price_sum = 0
    cw = [5, 6, 11, 6, 7, 4, 0, 9, 6, 7, 5]
    veCRV_mine = round(call_me(vecrv_func.balanceOf(MY_WALLET_ADDRESS))/10**18, 2)
    veCRV_total = round(call_me(vecrv_func.totalSupply())/10**18, 2)
    for i in range(0, len(carray["name"])):
        if carray["currentboost"][i] > 0 or fullheader:
            carray["totalsupply"][i] = round(call_me(load_contract(carray["guageaddress"][i],w3).totalSupply())/10**18, 2)
            carray["virtprice"][i] = round(call_me(load_contract(carray["swapaddress"][i],w3).get_virtual_price())/10**18, 6)
            carray["balanceof"][i] = round(call_me(load_contract(carray["guageaddress"][i],w3).balanceOf(MY_WALLET_ADDRESS))/10**18, 2)
            if len(carray["tokenaddress"][i]) > 1:
                carray["balanceof"][i] += round(call_me(load_contract(carray["tokenaddress"][i],w3).balanceOf(MY_WALLET_ADDRESS))/10**18, 2)
            virutal_price_sum += carray["virtprice"][i]*carray["balanceof"][i]*carray["token_value_modifyer"][i]
            maxinvestforfullboost = carray["totalsupply"][i]*veCRV_mine/veCRV_total
            print(carray["longname"][i].ljust(len(max(carray["longname"], key=len))), carray["name"][i], end=' ')
            print(str(format(carray["totalsupply"][i], ',.0f')).rjust(cw[2]), end=' ')
            print("|", end=' ')
            if carray["invested"][i] > 0:
                print(str(carray["invested"][i]).rjust(cw[0]), end=' ')
            else:
                print(" "*cw[0], end=' ')

            if carray["virtprice"][i]*carray["balanceof"][i]*carray["token_value_modifyer"][i] > 0:
                print(Style.DIM+Fore.GREEN+str(format((carray["virtprice"][i]*carray["balanceof"][i]*carray["token_value_modifyer"][i])-carray["invested"][i], '.2f')).rjust(cw[1])+Style.RESET_ALL, end=' ')
            else:
                print(" "*cw[1], end=' ')

            base_percent = ((carray["virtprice"][i]*carray["balanceof"][i]*carray["token_value_modifyer"][i])-carray["invested"][i])/(carray["invested"][i]+.00000001)*100
            if base_percent > 0 and carray["currentboost"][i] > 0:
                print("("+str(format(round(base_percent,3), '.3f')).rjust(5)+"%)", end=' ')
            else:
                print(" "*8, end=' ')
            #needed_veCRV = round((carray["balanceof"][i]/carray["totalsupply"][i]*veCRV_total)-veCRV_mine)
            carray["futureboost"][i] = 2.5*min((carray["balanceof"][i]/2.5) + (maxinvestforfullboost*(1-(1/2.5))), carray["balanceof"][i])/max(1,carray["balanceof"][i])
            #print(Style.DIM+str(format(round(carray["minted"][i]/10**18, 2), '.2f')).rjust(cw[4])+Style.RESET_ALL, end=' ')
            print("|", end=' ')
            if carray["currentboost"][i] >= 2.47:
                if carray["futureboost"][i]-carray["currentboost"][i] < 0:
                    #print(Style.DIM+Fore.GREEN+str(format(abs(round(maxinvestforfullboost-carray["balanceof"][i], 2)), '.2f')).rjust(cw[7])+Style.RESET_ALL, end=' ')
                    print(Style.BRIGHT+Fore.GREEN+str(format(carray["currentboost"][i], '.4f')).rjust(cw[8]).replace("0", " ")+Style.RESET_ALL, end=' ')
                    print(Style.DIM+Fore.GREEN+str(format(carray["futureboost"][i]-carray["currentboost"][i], '.4f')).rjust(cw[9])+Style.RESET_ALL, end=' ')
                    #print(Style.DIM+str(needed_veCRV).rjust(cw[10]), "additional veCRV needed to maintain full boost."+Style.RESET_ALL)
                    print("")
                else:
                    print(Style.BRIGHT+Fore.GREEN+str(format(carray["currentboost"][i], '.4f')).rjust(cw[8]).replace("0", " ")+Style.RESET_ALL, end=' ')
                    #print(" "*cw[9], end=' ')
                    print(("$"+str(format((maxinvestforfullboost-carray["balanceof"][i])*carray["token_value_modifyer"][i], '.0f'))).ljust(5)+Style.RESET_ALL, "fits   ", end='')
            elif carray["currentboost"][i] > 0:
                #print(Style.DIM+str(format(round(maxinvestforfullboost-carray["balanceof"][i], 2), '.2f')).rjust(cw[7])+Style.RESET_ALL, end=' ')
                print(str(format(carray["currentboost"][i], '.4f')).rjust(cw[8]), end=' ')
                if carray["futureboost"][i]-carray["currentboost"][i] <= 0:
                    print(Style.DIM+Fore.GREEN+str(format(carray["futureboost"][i]-carray["currentboost"][i], '.4f')).rjust(cw[9])+Style.RESET_ALL, end=' ')
                elif carray["futureboost"][i]-carray["currentboost"][i] < 0.05:
                    print(Style.DIM+Fore.RED+str(format(carray["futureboost"][i]-carray["currentboost"][i], '.4f')).rjust(cw[9])+Style.RESET_ALL, end=' ')
                else:
                    print(Style.BRIGHT+Fore.RED+str(format(carray["futureboost"][i]-carray["currentboost"][i], '.4f')).rjust(cw[9])+Style.RESET_ALL, end=' ')
                #print(Style.DIM+str(needed_veCRV).rjust(cw[10]), "additional veCRV needed for full boost."+Style.RESET_ALL)
                print("     ",end='')
#            print("|", end=' ')
#            print(str(format(round(myarray[-1][carray["name"][i]+"pool"], 2), '.0f')).rjust(cw[5]), end=' ')
            #print(" "*7, end='')
            if abs(round(myarray[-1][carray["name"][i]+"pool"]-round(carray["minted"][i]/10**18,2), 2)) > 0.1:
                print(Style.DIM+Fore.CYAN+str(format(round(myarray[-1][carray["name"][i]+"pool"]-(round(carray["minted"][i]/10**18,2)), 2), '.2f')).rjust(cw[3])+Style.RESET_ALL, end=' ')
            else:
                print(" "*cw[3], end=' ')
            if abs(round(myarray[-1][carray["name"][i]+"pool"]-round(carray["minted"][i]/10**18,2), 2)) > 0.1:
                print("$"+str(format(round((myarray[-1][carray["name"][i]+"pool"]-(round(carray["minted"][i]/10**18,2)))*myarray[-1]["USD"], 2), '5.2f')).rjust(6)+Style.RESET_ALL, end=' ')
            print("")
    return virutal_price_sum

def combined_stats_display(myarray, carray, w3, virutal_price_sum):
    crv_func = load_contract("0xD533a949740bb3306d119CC777fa900bA034cd52",w3)
    vecrv_func = load_contract("0x5f3b5DfEb7B28CDbD7FAba78963EE202a494e2A2",w3)
    cvx_token = load_contract("0x4e3FBD56CD56c3e72c1403e103b45Db9da5B9D2B",w3)
    cvxcrv_token = load_contract("0x62B9c7356A2Dc64a1969e19C23e4f579F9810Aa7",w3)
    crv3pool_token = load_contract("0x6c3F90f043a72FA612cbac8115EE7e52BDe6E490",w3)

    CRV_inwallet = round(call_me(crv_func.balanceOf(MY_WALLET_ADDRESS))/10**18)
    cvx_inwallet = round(call_me(cvx_token.balanceOf(MY_WALLET_ADDRESS))/10**18)
    cvxcrv_inwallet = round(call_me(cvxcrv_token.balanceOf(MY_WALLET_ADDRESS))/10**18)
    crv3pool_inwallet = round(call_me(crv3pool_token.balanceOf(MY_WALLET_ADDRESS))/10**18)

    veCRV_mine = round(call_me(vecrv_func.balanceOf(MY_WALLET_ADDRESS))/10**18)
    veCRV_locked = round(call_me(vecrv_func.locked(MY_WALLET_ADDRESS))/10**18)
    x_claimable = (myarray[-1]["cvx_rewards"][3]*(myarray[-1]["USD3pool"]/myarray[-1]["USD"]))+\
                  (myarray[-1]["cvx_rewards"][2]*(myarray[-1]["USDcvx"]/myarray[-1]["USD"]))+\
                  myarray[-1]["cvx_rewards"][1]+\
                  (myarray[-1]["trix_rewards"][2]*(myarray[-1]["USDcvx"]/myarray[-1]["USD"]))+\
                  myarray[-1]["trix_rewards"][1]+\
                  myarray[-1]["cvxcrv_rewards"][1]
    sushi_claimable = (myarray[-1]["cvxsushi_rewards"][1]*(myarray[-1]["USDcvx"]/myarray[-1]["USD"]))
    print("$"+str(sum(carray["invested"])+(myarray[-1]["trix_rewards"][0]*carray["token_value_modifyer"][carray["longname"].index("tRicrypto")])), "invested,",sum(carray["invested"]),"is now",int(virutal_price_sum), end=' ')
    print("("+str(format(round(( virutal_price_sum/sum(carray["invested"])*100)-100,5),'.3f'))+"%)  ", end=' ')
    print("Ç"+str(round(veCRV_locked)), "veCRV locked" +Style.DIM+" ("+str(veCRV_mine), "voting)   "+Style.RESET_ALL, end='')
    #print(csym+str(round(sum(carray["minted"])/10**18, 2))+Style.RESET_ALL, "minted ", end=' ')
    print("$"+str(format(round((myarray[-1]["claim"]-(sum(carray["minted"])/10**18)+x_claimable+sushi_claimable)*myarray[-1]["USD"], 2),'5.2f')).rjust(6)+Style.RESET_ALL,("("+str(round(x_claimable*myarray[-1]["USD"]))+") to claim  ").rjust(17), end=' ')
    show_wallet(CRV_inwallet, cvxcrv_inwallet, cvx_inwallet, crv3pool_inwallet)

    eoa = 0 - len(myarray)
    if round((round(time.time())-myarray[eoa]["raw_time"])/60, 2)+eoa >= 0.5:
        print(Fore.RED+str(round(((round(time.time())-myarray[eoa]["raw_time"])/60)+eoa, 2))+Style.RESET_ALL+"oos", end=' ')
    if eoa > -61:
        print(Style.BRIGHT+Fore.RED+str(61+eoa)+Style.RESET_ALL+" minutes under 60.", end=' ')
    if sum(carray["invested"]) != myarray[eoa]["invested"]:
        print(Fore.RED+str(sum(carray["invested"]) - myarray[eoa]["invested"])+Style.RESET_ALL+" of New $ obs. data", end='')
    if myarray[-1]["cvx_rewards"][0] != myarray[eoa]["cvx_rewards"][0]:
        print(Fore.RED+str(myarray[-1]["cvx_rewards"][0] - myarray[eoa]["cvx_rewards"][0])+Style.RESET_ALL+" of New $ obs. data", end=' ')
    if myarray[-1]["trix_rewards"][0] != myarray[eoa]["trix_rewards"][0]:
        print(Fore.RED+str(myarray[-1]["trix_rewards"][0] - myarray[eoa]["trix_rewards"][0])+Style.RESET_ALL+" of New $ obs. data", end=' ')
    print("")

def show_wallet(CRV_inwallet,cvxcrv_inwallet,cvx_inwallet,crv3pool_inwallet):
    print("[", end='')
    if CRV_inwallet > 0:
        print(csym+f"{CRV_inwallet:02}"+Style.RESET_ALL, end='')
    if cvxcrv_inwallet > 0:
        print("v"+csym+f"{cvxcrv_inwallet:02}"+Style.RESET_ALL, end='')
    if cvx_inwallet > 0:
        print("x"+Fore.BLUE+f"{cvx_inwallet:02}"+Style.RESET_ALL, end='')
    if crv3pool_inwallet > 0:
        print("t"+Fore.YELLOW+Style.BRIGHT+f"{crv3pool_inwallet:02}"+Style.RESET_ALL, end='')
    print("] in wallet ", end='  ')

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
    for i in range(0, len(thisarray)):
        barray["longname"].append(thisarray[i]["longname"])
        barray["invested"].append(thisarray[i]["invested"])
        barray["currentboost"].append(thisarray[i]["currentboost"])
        barray["name"].append(thisarray[i]["name"])
        barray["guageaddress"].append(thisarray[i]["guageaddress"])
        barray["swapaddress"].append(thisarray[i]["swapaddress"])
        try:
            barray["minted"][i] = call_me(minter_func.minted(MY_WALLET_ADDRESS, barray["guageaddress"][i]))
            barray["tokenaddress"].append(thisarray[i]["tokenaddress"])
        except Exception:
            barray["tokenaddress"].append("")
        try:
            _ = myarray[-1][barray["name"][i]+"pool"]
        except Exception:
            print(thisarray[i]["longname"], "not found in current history file, adding now.")
            myarray[-1][barray["name"][i]+"pool"] = 0
            myarray[-1][barray["name"][i]+"invested"] = 0
        try:
            barray["token_value_modifyer"][i] = thisarray[i]["token_value_modifyer"]
        except Exception:
            barray["token_value_modifyer"][i] = 1

def update_curve_pools(mydict,carray,myarray,myarrayh,w3):
    minter_func = load_contract("0xd061D61a4d941c39E5453435B6345Dc261C2fcE0",w3)
    for i in range(0, len(carray["name"])):
        mydict[carray["name"][i]+"invested"] = carray["invested"][i]
        try:
            if carray["invested"][i] > 0: #skip updating empty pools
                carray["balanceof"][i] = call_me(load_contract(carray["guageaddress"][i],w3).balanceOf(MY_WALLET_ADDRESS))/10**18
                time.sleep(0.1)
                carray["raw"][i] = call_me(load_contract(carray["guageaddress"][i],w3).claimable_tokens(MY_WALLET_ADDRESS))
                potential_virtprice_update = call_me(load_contract(carray["swapaddress"][i],w3).get_virtual_price())/10**18
                mydict[carray["name"][i]+"virtprice"] = potential_virtprice_update
                if potential_virtprice_update > carray["virtprice"][i]:
                    carray["virtprice"][i] = potential_virtprice_update
                if (carray["virtprice"][i]*carray["balanceof"][i]*carray["token_value_modifyer"][i])-carray["invested"][i] > -10:
                    mydict[carray["name"][i]+"profit"] = (carray["virtprice"][i]*carray["balanceof"][i]*carray["token_value_modifyer"][i])-carray["invested"][i]
            if abs(round((carray["raw"][i]+carray["minted"][i])/10**18, 5) - myarray[-1][carray["name"][i]+"pool"]) > 10:
                print("\nMINTING HAPPENED:", carray["name"][i], "pool      Before", carray["minted"][i], end='   ')
                carray["minted"][i] = call_me(minter_func.minted(MY_WALLET_ADDRESS, carray["guageaddress"][i]))
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
    try:
        vecrv_func = load_contract("0x5f3b5DfEb7B28CDbD7FAba78963EE202a494e2A2",w3)
        veCRV_mine = round(call_me(vecrv_func.balanceOf(MY_WALLET_ADDRESS))/10**18, 2)
        veCRV_total = round(call_me(vecrv_func.totalSupply())/10**18, 2)
        outputflag = 0
        for i in range(0, len(carray["name"])):
            if carray["currentboost"][i] >= 2.47:   #hack to avoid spool which is annoyingly close to 2.5 boost
                carray["booststatus"][i] = -1               #Green, all is well
            elif carray["currentboost"][i] == 0:
                carray["booststatus"][i] = 4                #Blue, pool is empty
            else:
                carray["balanceof"][i] = round(call_me(load_contract(carray["guageaddress"][i],w3).balanceOf(MY_WALLET_ADDRESS))/10**18, 2)
                carray["totalsupply"][i] = round(call_me(load_contract(carray["guageaddress"][i],w3).totalSupply())/10**18, 2)
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
            print(Fore.GREEN+'Bööst'+Style.RESET_ALL, end=' ')
    except Exception:
        print("uperr", end=' ')

if __name__ == "__main__":
    print("this module is not meant to be run solo")
