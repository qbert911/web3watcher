#!/usr/bin/env python3
"""curve"""
# pylint: disable=C0103,C0301,W0105,E0401,R0914,C0411,W0702,C0200,C0116,w0106
import json
import time
from colorama import Fore, Style
from load_contract import load_contract, call_me

MY_WALLET_ADDRESS = "0x8D82Fef0d77d79e5231AE7BFcFeBA2bAcF127E2B"
csym = Fore.MAGENTA + Style.BRIGHT + "Ç" + Style.RESET_ALL + Fore.CYAN

def curve_header_display(myarray, carray, w3, fullheader):
    """display detailed pool information"""
    vecrv_func = load_contract("0x5f3b5DfEb7B28CDbD7FAba78963EE202a494e2A2",w3)
    crv_func = load_contract("0xD533a949740bb3306d119CC777fa900bA034cd52",w3)
    virutal_price_sum = 0
    cw = [5, 6, 11, 6, 7, 4, 0, 9, 6, 7, 5]
    CRV_inwallet = round(call_me(crv_func.balanceOf(MY_WALLET_ADDRESS))/10**18, 2)
    veCRV_locked = round(call_me(vecrv_func.locked(MY_WALLET_ADDRESS))/10**18, 2)
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
            print("|", end=' ')
            #needed_veCRV = round((carray["balanceof"][i]/carray["totalsupply"][i]*veCRV_total)-veCRV_mine)
            carray["futureboost"][i] = 2.5*min((carray["balanceof"][i]/2.5) + (maxinvestforfullboost*(1-(1/2.5))), carray["balanceof"][i])/max(1,carray["balanceof"][i])
            print(str(format(round(myarray[-1][carray["name"][i]+"pool"], 2), '.0f')).rjust(cw[5]), end=' ')
            if abs(round(myarray[-1][carray["name"][i]+"pool"]-round(carray["minted"][i]/10**18,2), 2)) > 0.1:
                print(Style.DIM+Fore.CYAN+str(format(round(myarray[-1][carray["name"][i]+"pool"]-(round(carray["minted"][i]/10**18,2)), 2), '.2f')).rjust(cw[3])+Style.RESET_ALL, end=' ')
            else:
                print(" "*cw[3], end=' ')
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
                    print(" "*cw[9], end=' ')
                    print(("$"+str(format(round(maxinvestforfullboost-carray["balanceof"][i]), '.0f'))).rjust(cw[10])+Style.RESET_ALL, "can still fit")
            elif carray["currentboost"][i] > 0:
                #print(Style.DIM+str(format(round(maxinvestforfullboost-carray["balanceof"][i], 2), '.2f')).rjust(cw[7])+Style.RESET_ALL, end=' ')
                print(str(format(carray["currentboost"][i], '.4f')).rjust(cw[8]), end=' ')
                if carray["futureboost"][i]-carray["currentboost"][i] <= 0:
                    print(Style.DIM+Fore.GREEN+str(format(carray["futureboost"][i]-carray["currentboost"][i], '.4f')).rjust(cw[9])+Style.RESET_ALL, end=' ')
                elif carray["futureboost"][i]-carray["currentboost"][i] < 0.05:
                    print(Style.DIM+Fore.RED+str(format(carray["futureboost"][i]-carray["currentboost"][i], '.4f')).rjust(cw[9])+Style.RESET_ALL, end=' ')
                else:
                    print(Style.BRIGHT+Fore.RED+str(format(carray["futureboost"][i]-carray["currentboost"][i], '.4f')).rjust(cw[9])+Style.RESET_ALL, end=' ')
                print("")
                #print(Style.DIM+str(needed_veCRV).rjust(cw[10]), "additional veCRV needed for full boost."+Style.RESET_ALL)
            else:
                print("")

    print("$"+str(sum(carray["invested"])+(myarray[-1]["trix_rewards"][0]*carray["token_value_modifyer"][0])), "invested,",sum(carray["invested"]),"is now",int(virutal_price_sum), end=' ')
    print("("+str(format(round(( virutal_price_sum/sum(carray["invested"])*100)-100,5),'.3f'))+"%)", end='   ')
    print("Ç"+str(round(veCRV_locked)), "veCRV locked" +Style.DIM+" ("+str(veCRV_mine), "voting)"+Style.RESET_ALL, end='  ')
    print(csym+str(round(sum(carray["minted"])/10**18, 2))+Style.RESET_ALL, "minted", end=' ')
    print(csym+str(round(myarray[-1]["claim"]-(sum(carray["minted"])/10**18), 2))+Style.RESET_ALL, "in gauge", end=' ')
    print("("+csym+str(CRV_inwallet)+Style.RESET_ALL,"wallet)", end='  ')

    eoa = 0 - len(myarray)
    if round((round(time.time())-myarray[eoa]["raw_time"])/60, 2)+eoa >= 0.5:
        print(Fore.RED+str(round(((round(time.time())-myarray[eoa]["raw_time"])/60)+eoa, 2))+Style.RESET_ALL+" min oos.", end=' ')
    if eoa > -61:
        print(Fore.RED+str(61+eoa)+Style.RESET_ALL+" minutes under 60.", end=' ')
    if sum(carray["invested"]) != myarray[eoa]["invested"]:
        print(Fore.RED+str(sum(carray["invested"]) - myarray[eoa]["invested"])+Style.RESET_ALL+" of New $ obs. data", end='')
    print("")


def load_curvepool_array(myarray,barray,w3):
    """prepare iteratable array from json file"""
    with open("curvepools.json", 'r') as thisfile:
        thisarray = json.load(thisfile)
    minter_func = load_contract("0xd061D61a4d941c39E5453435B6345Dc261C2fcE0",w3)

    barray["minted"] = [0]*len(thisarray)
    barray["balanceof"] = [0]*len(thisarray)
    barray["raw"] = [1]*len(thisarray)
    barray["totalsupply"] = [0]*len(thisarray)
    barray["futureboost"] = [0]*len(thisarray)
    barray["booststatus"] = [0]*len(thisarray)
    barray["virtprice"] = [0]*len(thisarray)
    barray["token_value_modifyer"] = [0]*len(thisarray)
    print(len(thisarray),"pools loaded from curvepools.json")
    #print(thisarray,flush=True)
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
        except:
            barray["tokenaddress"].append("")
        try:
            _ = myarray[-1][barray["name"][i]+"pool"]
        except:
            print(thisarray[i]["longname"], "not found in current history file, adding now.")
            myarray[-1][barray["name"][i]+"pool"] = 0
            myarray[-1][barray["name"][i]+"invested"] = 0
        try:
            barray["token_value_modifyer"][i] = thisarray[i]["token_value_modifyer"]
        except:
            barray["token_value_modifyer"][i] = 1


def update_curve_pools(mydict,carray,myarray,myarrayh,w3):
    minter_func = load_contract("0xd061D61a4d941c39E5453435B6345Dc261C2fcE0",w3)
    for i in range(0, len(carray["name"])):
        mydict[carray["name"][i]+"invested"] = carray["invested"][i]
        try:
            if carray["raw"][i] > 0: #skip updating empty pools after the initial check
                carray["raw"][i] = call_me(load_contract(carray["guageaddress"][i],w3).claimable_tokens(MY_WALLET_ADDRESS))
                potential_virtprice_update = call_me(load_contract(carray["swapaddress"][i],w3).get_virtual_price())/10**18
                if potential_virtprice_update > carray["virtprice"][i]:
                    carray["virtprice"][i] = potential_virtprice_update
                carray["balanceof"][i] = call_me(load_contract(carray["guageaddress"][i],w3).balanceOf(MY_WALLET_ADDRESS))/10**18
                if (carray["virtprice"][i]*carray["balanceof"][i]*carray["token_value_modifyer"][i])-carray["invested"][i] > -10:
                    mydict[carray["name"][i]+"profit"] = (carray["virtprice"][i]*carray["balanceof"][i]*carray["token_value_modifyer"][i])-carray["invested"][i]
            if abs(round((carray["raw"][i]+carray["minted"][i])/10**18, 5) - myarray[-1][carray["name"][i]+"pool"]) > 3:
                print("\nMINTING HAPPENED:", carray["name"][i], "pool      Before", carray["minted"][i], end='   ')
                carray["minted"][i] = call_me(minter_func.minted(MY_WALLET_ADDRESS, carray["guageaddress"][i]))
                print("After", carray["minted"][i])
            mydict[carray["name"][i]+"pool"] = round((carray["raw"][i]+carray["minted"][i])/10**18, 5)
            if myarray[-1][carray["name"][i]+"pool"] - mydict[carray["name"][i]+"pool"] > 0.01: #debug lines ... should not happen
                print(myarray[-1][carray["name"][i]+"pool"] - mydict[carray["name"][i]+"pool"], "\nerror with lower raw value"+carray["name"][i], myarray[-1][carray["name"][i]+"pool"], mydict[carray["name"][i]+"pool"], end='')
        except: #usually happens when snx is down for maintenance
            mydict[carray["name"][i]+"pool"] = myarrayh[-1][carray["name"][i]+"pool"]
            carray["raw"][i] = (myarrayh[-1][carray["name"][i]+"pool"]*10**18) - carray["minted"][i]
    mydict["claim"] = round((sum(carray["raw"])+sum(carray["minted"]))/10**18, 6)

def curve_boost_check(carray,w3):
    """update variables to check boost status"""
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
