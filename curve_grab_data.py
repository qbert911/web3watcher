#!/usr/bin/env python3
"""curve"""
# pylint: disable=C0103,C0301,W0105,E0401,R0914,C0411,W0702,C0200
import json
import time
import logging
import cursor
import threading
import argparse
from colorama import Back, Fore, Style, init
from curve_log_process import show_me, update_price
logging.getLogger().disabled = True
from web3 import Web3
logging.getLogger().disabled = False
try:
    from curve_rainbowhat_functions import curve_hats_update
except:
    print("No Raspberry Pi Hats Found.")
    pass

cursor.hide()
init()

MY_WALLET_ADDRESS = "0x8D82Fef0d77d79e5231AE7BFcFeBA2bAcF127E2B"
INFURA_ID = "6aa1a043a9854eaa9fa68d17f619f326"

abiguage = json.load(open("abi_bfcf.json", 'r'))
abiminter = json.load(open("abi_d061.json", 'r'))
abivoting = json.load(open("abi_5f3b.json", 'r'))
abivirtprice = json.load(open("abi_a540.json", 'r'))
MINTER_ADDRESS = "0xd061D61a4d941c39E5453435B6345Dc261C2fcE0"
veCRV_ADDRESS = "0x5f3b5DfEb7B28CDbD7FAba78963EE202a494e2A2"
CRV_ADDRESS = "0xD533a949740bb3306d119CC777fa900bA034cd52"

abifulcrum = json.load(open("abi_d172.json", 'r'))
abicream = json.load(open("abi_c7fd.json", 'r'))
abiaave2 = json.load(open("abi_c684.json", 'r'))
abisplus = json.load(open("abi_a909.json", 'r')) #as yet unused - SNX?

file_name = "ghistory.json"
file_nameh = "ghistoryh.json"
myarray = json.load(open(file_name, 'r'))
myarrayh = json.load(open(file_nameh, 'r'))
carray = {"longname": [], "name": [], "invested": [], "currentboost": [], "address" : [], "tokenaddress" : []}

csym = Fore.MAGENTA + Style.BRIGHT + "Ç" + Style.RESET_ALL + Fore.CYAN
TARGET_AMOUNT = 10
enter_hit = False

parser = argparse.ArgumentParser()
parser.add_argument("-l", "--Local", help = "Local Node Used", action="store_true")
parser.add_argument("-r", "--Readonly", help = "Don't write output to file", action="store_true")
args = parser.parse_args()
print("Read Only Mode:",args.Readonly)
if args.Local:
    w3 = Web3(Web3.HTTPProvider('http://172.33.0.2:8545'))
    print("Data Source: LOCAL")
else:
    print("Data Source: Infura")
    w3 = Web3(Web3.HTTPProvider('https://mainnet.infura.io/v3/'+INFURA_ID))

def key_capture_thread():
    global enter_hit
    input()
    enter_hit = True

def call_me(function):
    """input filtering"""
    x = function.call()
    if isinstance(x, list):
        x = x[0]
    if x < 10000:
        print("\n odd output when calling "+str(function),x)
    return x

def show_additional_pool_coins():
    a=round(call_me(w3.eth.contract("0xA90996896660DEcC6E997655E065b23788857849", abi=abisplus).functions.claimable_reward(MY_WALLET_ADDRESS))/10**18, 4)
    print(Back.CYAN+Fore.BLUE+Style.DIM+"S "+str(format(a, '.3f')).lstrip("0")+Style.RESET_ALL, end=' - ')

def show_other_exchanges():
    #iusdc_interest = round(w3.eth.contract("0x32E4c68B3A4a813b710595AebA7f6B7604Ab9c15", abi=abifulcrum).functions.nextSupplyInterestRate(1).call()/10**18, 2)
    crcrv_interest = round(((((w3.eth.contract("0xc7Fd8Dcee4697ceef5a2fd4608a7BD6A94C77480", abi=abicream).functions.supplyRatePerBlock().call()*4*60*24/10**18)+1)**364)-1)*100, 2)
    #crusdc_interest = round(((((w3.eth.contract("0x44fbeBd2F576670a6C33f6Fc0B00aA8c5753b322", abi=abicream).functions.supplyRatePerBlock().call()*4*60*24/10**18)+1)**364)-1)*100, 2)
    aacrv_interest = round(w3.eth.contract("0x7d2768dE32b0b80b7a3454c06BdAc94A69DDc7A9", abi=abiaave2).functions.getReserveData("0xD533a949740bb3306d119CC777fa900bA034cd52").call()[3]/10**25,2)
    print(Back.CYAN+Fore.BLUE+Style.DIM+
          "A"+str(format(aacrv_interest, '05.1f'))+"%",
          "C"+str(format(crcrv_interest, '05.2f'))+"%"+Style.RESET_ALL, end=' - ')  #+"C"+str(crusdc_interest)+"% "+Fore.MAGENTA+Style.BRIGHT+"Ç"+str(format(crcrv_interest, '.2f'))+"%"

def load_curvepool_array(barray):
    """prepare iteratable array from json file"""
    with open("curvepools.json", 'r') as thisfile:
        thisarray = json.load(thisfile)

    barray["minted"] = [0]*len(thisarray)
    barray["balanceof"] = [0]*len(thisarray)
    barray["raw"] = [0]*len(thisarray)
    barray["totalsupply"] = [0]*len(thisarray)
    barray["futureboost"] = [0]*len(thisarray)
    barray["booststatus"] = [0]*len(thisarray)
    barray["virtprice"] = [0]*len(thisarray)
    print(len(thisarray),"pools loaded from curvepools.json")
    #print(thisarray,flush=True)
    for i in range(0, len(thisarray)):
        barray["longname"].append(thisarray[i]["longname"])
        barray["invested"].append(thisarray[i]["invested"])
        barray["currentboost"].append(thisarray[i]["currentboost"])
        barray["name"].append(thisarray[i]["name"])
        barray["address"].append(thisarray[i]["address"])
        barray["tokenaddress"].append(thisarray[i]["tokenaddress"])
        if barray["currentboost"][i] > 0:
            barray["minted"][i] = call_me(w3.eth.contract(MINTER_ADDRESS, abi=abiminter).functions.minted(MY_WALLET_ADDRESS, carray["address"][i]))

def header_display():
    """display detailed pool information"""
    cw = [5, 8, 9, 6, 7, 7, 5, 9, 6, 7, 5]
    CRV_inwallet = round(call_me(w3.eth.contract(CRV_ADDRESS, abi=abivoting).functions.balanceOf(MY_WALLET_ADDRESS))/10**18, 2)
    veCRV_locked = round(call_me(w3.eth.contract(veCRV_ADDRESS, abi=abivoting).functions.locked(MY_WALLET_ADDRESS))/10**18, 2)
    veCRV_mine = round(call_me(w3.eth.contract(veCRV_ADDRESS, abi=abivoting).functions.balanceOf(MY_WALLET_ADDRESS))/10**18, 2)
    veCRV_total = round(call_me(w3.eth.contract(veCRV_ADDRESS, abi=abivoting).functions.totalSupply())/10**18, 2)
    for i in range(0, len(carray["name"])):
        carray["totalsupply"][i] = round(call_me(w3.eth.contract(carray["address"][i], abi=abiguage).functions.totalSupply())/10**18, 2)
        carray["virtprice"][i] = round(call_me(w3.eth.contract(carray["tokenaddress"][i], abi=abivirtprice).functions.get_virtual_price())/10**18, 6)
        if carray["currentboost"][i] > 0:
            carray["balanceof"][i] = round(call_me(w3.eth.contract(carray["address"][i], abi=abiguage).functions.balanceOf(MY_WALLET_ADDRESS))/10**18, 2)
        maxinvestforfullboost = carray["totalsupply"][i]*veCRV_mine/veCRV_total
        print(carray["longname"][i].ljust(len(max(carray["longname"], key=len))), carray["name"][i],
              str(carray["invested"][i]).rjust(cw[0]),
              str(format(carray["virtprice"][i]*carray["balanceof"][i], '.2f')).rjust(cw[1]),
              str(format(carray["totalsupply"][i], '.0f')).rjust(cw[2]), end=' ')
        if carray["currentboost"][i] > 0:
            needed_veCRV = round((carray["balanceof"][i]/carray["totalsupply"][i]*veCRV_total)-veCRV_mine)
            carray["futureboost"][i] = 2.5*min((carray["balanceof"][i]/2.5) + (maxinvestforfullboost*(1-(1/2.5))), carray["balanceof"][i])/carray["balanceof"][i]
            print(Style.DIM+str(format(round(myarray[-1][carray["name"][i]+"pool"]-(carray["minted"][i]/10**18), 2), '.2f')).rjust(cw[3])+Style.RESET_ALL,
                  Style.DIM+str(format(round(carray["minted"][i]/10**18, 2), '.2f')).rjust(cw[4])+Style.RESET_ALL,
                  str(format(round(myarray[-1][carray["name"][i]+"pool"], 2), '.2f')).rjust(cw[5]),
                  str(format(round(myarray[-1][carray["name"][i]+"pool"]/myarray[-1][carray["name"][i]+"invested"]*100, 2), '.2f')).rjust(cw[6])+"%", end=' ')
        else:
            needed_veCRV = round((TARGET_AMOUNT/carray["totalsupply"][i]*veCRV_total)-veCRV_mine)
            print(Style.DIM+str(format(round(0, 2), '.2f')).rjust(cw[3])+Style.RESET_ALL,
                  Style.DIM+str(format(round(carray["minted"][i]/10**18, 2), '.2f')).rjust(cw[4])+Style.RESET_ALL,
                  str(format(round(0, 2), '.2f')).rjust(cw[5]),
                  str(format(round(0, 2), '.2f')).rjust(cw[6])+"%", end=' ')

        if carray["currentboost"][i] >= 2.5:
            if carray["futureboost"][i]-carray["currentboost"][i] < 0:
                print(Style.DIM+Fore.GREEN+str(format(abs(round(maxinvestforfullboost-carray["balanceof"][i], 2)), '.2f')).rjust(cw[7])+Style.RESET_ALL, end=' ')
                print(Style.BRIGHT+Fore.GREEN+str(format(carray["currentboost"][i], '.4f')).rjust(cw[8]).replace("0", " ")+Style.RESET_ALL, end=' ')
                print(Style.DIM+Fore.GREEN+str(format(carray["futureboost"][i]-carray["currentboost"][i], '.4f')).rjust(cw[9])+Style.RESET_ALL, end=' ')
                print(Style.DIM+str(needed_veCRV).rjust(cw[10]), "additional veCRV needed to maintain full boost."+Style.RESET_ALL)
            else:
                print(str(format(round(maxinvestforfullboost-carray["balanceof"][i], 2), '.2f')).rjust(cw[7])+Style.RESET_ALL, end=' ')
                print(Style.BRIGHT+Fore.GREEN+str(format(carray["currentboost"][i], '.4f')).rjust(cw[8]).replace("0", " ")+Style.RESET_ALL)
        else:
            print(Style.DIM+str(format(round(maxinvestforfullboost-carray["balanceof"][i], 2), '.2f')).rjust(cw[7])+Style.RESET_ALL, end=' ')
            print(str(format(carray["currentboost"][i], '.4f')).rjust(cw[8]), end=' ')
            if carray["futureboost"][i]-carray["currentboost"][i] <= 0:
                print(Style.DIM+Fore.GREEN+str(format(carray["futureboost"][i]-carray["currentboost"][i], '.4f')).rjust(cw[9])+Style.RESET_ALL, end=' ')
            else:
                if carray["futureboost"][i]-carray["currentboost"][i] >= 0.05:
                    print(Style.BRIGHT+Fore.RED+str(format(carray["futureboost"][i]-carray["currentboost"][i], '.4f')).rjust(cw[9])+Style.RESET_ALL, end=' ')
                else:
                    print(Style.DIM+Fore.RED+str(format(carray["futureboost"][i]-carray["currentboost"][i], '.4f')).rjust(cw[9])+Style.RESET_ALL, end=' ')
            if carray["currentboost"][i] == 0:
                print(str(needed_veCRV).rjust(cw[10]), "additional veCRV needed for full boost at target of $"+str(TARGET_AMOUNT))
            else:
                print(str(needed_veCRV).rjust(cw[10]), "additional veCRV needed for full boost.")

    print(sum(carray["invested"]), "invested, as well as", veCRV_mine, "veCRV voting"+Style.DIM+" (from", veCRV_locked, "locked)"+Style.RESET_ALL, end='  ')
    print(csym+str(round(myarray[-1]["claim"]-(sum(carray["minted"])/10**18), 2))+Style.RESET_ALL, "in pools ",end=' ')
    print(csym+str(round(sum(carray["minted"])/10**18, 2))+Style.RESET_ALL, "minted ", end=' ')
    print(csym+str(CRV_inwallet)+Style.RESET_ALL,"on sidelines", end='  ')

    eoa = 0 - len(myarray)
    if round((round(time.time())-myarray[eoa]["raw_time"])/60, 2)+eoa >= 0.5:
        print(Fore.RED+str(round(((round(time.time())-myarray[eoa]["raw_time"])/60)+eoa, 2))+Style.RESET_ALL+" minutes out of sync.", end=' ')
    if eoa > -61:
        print(Fore.RED+str(61+eoa)+Style.RESET_ALL+" minutes under 60.", end=' ')
    if sum(carray["invested"]) != myarray[eoa]["invested"]:
        print(Fore.RED+str(sum(carray["invested"]) - myarray[eoa]["invested"])+Style.RESET_ALL+" of New $ obs. data", end='')
    print("")
    global enter_hit
    enter_hit=False
    threading.Thread(target=key_capture_thread, args=(), name='key_capture_thread', daemon=True).start()

def boost_check(endchar):
    """update variables to check boost status"""
    veCRV_mine = round(call_me(w3.eth.contract(veCRV_ADDRESS, abi=abivoting).functions.balanceOf(MY_WALLET_ADDRESS))/10**18, 2)
    veCRV_total = round(call_me(w3.eth.contract(veCRV_ADDRESS, abi=abivoting).functions.totalSupply())/10**18, 2)
    outputflag = 0
    for i in range(0, len(carray["name"])):
        if carray["currentboost"][i] == 2.5:
            carray["booststatus"][i] = -1               #Green, all is well
        elif carray["currentboost"][i] == 0:
            carray["booststatus"][i] = 4                #Blue, pool is empty
        else:
            carray["balanceof"][i] = round(call_me(w3.eth.contract(carray["address"][i], abi=abiguage).functions.balanceOf(MY_WALLET_ADDRESS))/10**18, 2)
            carray["totalsupply"][i] = round(call_me(w3.eth.contract(carray["address"][i], abi=abiguage).functions.totalSupply())/10**18, 2)
            if carray["currentboost"][i] > 0:
                carray["futureboost"][i] = 2.5 * min((carray["balanceof"][i]/2.5) + (carray["totalsupply"][i]*veCRV_mine/veCRV_total*(1-(1/2.5))), carray["balanceof"][i])/carray["balanceof"][i]
            if carray["currentboost"][i] >= carray["futureboost"][i]:
                carray["booststatus"][i] = 1            #Gray, boost status was higher before, nothing to do
            else:
                outputflag = 1
                print(carray["name"][i], end='')
                if carray["futureboost"][i]-carray["currentboost"][i] >= .05:
                    carray["booststatus"][i] = 2        #Red, big enough change in boost status to care
                    print( #str(format(carray["futureboost"][i], '.4f')).rjust(6),
                          Style.BRIGHT+Fore.RED+str(format(carray["futureboost"][i]-carray["currentboost"][i], '.4f')).rjust(5).lstrip("0")+Style.RESET_ALL, end=' ')
                else:
                    carray["booststatus"][i] = 3        #Purple, small change in boost status
                    print( #str(format(carray["futureboost"][i], '.4f')).rjust(6),
                          Style.DIM+Fore.RED+str(format(carray["futureboost"][i]-carray["currentboost"][i], '.4f')).rjust(5).lstrip("0")+Style.RESET_ALL, end=' ')

    if outputflag:
        print('\b', end=endchar)
    else:
        print(Fore.GREEN+'Boosted'+Style.RESET_ALL, end=endchar)

def print_status_line(USD, eoa):
    """print main status line"""
    extramins = round((myarray[-1]["raw_time"]-myarray[eoa]["raw_time"])/60)+eoa
    difference = (myarray[-1]["claim"]-myarray[eoa]["claim"])/(60+extramins)*60
    print("\rAt $"+Fore.YELLOW+str(format(USD, '.3f'))+Fore.WHITE+" per CRV = "+
          Fore.GREEN+Style.BRIGHT+str(format(round((difference)*USD*24*365/sum(carray["invested"])*100, 2), '.2f'))+Style.NORMAL+Fore.WHITE+"/"+
          Fore.CYAN+str(format(round((difference)*24*365/sum(carray["invested"])*100, 2), '.2f'))+Fore.WHITE+"% APR", end=' ')

    for i in range(0, len(carray["name"])):
        if carray["currentboost"][i] > 0:
            print(Fore.RED+Style.BRIGHT+carray["name"][i]+Style.RESET_ALL+
                  str(format(round((myarray[-1][carray["name"][i]+"pool"]-myarray[eoa][carray["name"][i]+"pool"])/(60+extramins)*60*USD*24*365/carray["invested"][i]*100, 2), '.2f')), end=' ')

    print(csym+format(myarray[-1]["claim"], '.4f')+Style.RESET_ALL,
          "H"+csym+format((round(difference, 5)), '.5f')+Style.RESET_ALL,
          "D"+csym+format((round((difference)*24, 2)), '.2f')+Style.RESET_ALL,
          "Y"+csym+format((round((difference)*24*365, 0)), '.0f').rjust(5)+Style.RESET_ALL, end=' - ')
    print(myarray[-1]["human_time"], end=' - ')
    #show_other_exchanges()
    show_additional_pool_coins()
    boost_check(" - ")
    if extramins >= 0: #air bubble extra minutes
        print(Fore.RED+str(round((myarray[-1]["raw_time"]-myarray[eoa]["raw_time"])/60)+eoa+1)+Style.RESET_ALL, end=' - ')
    if eoa > -61:  #fewer than 60 records in the ghistory.json file
        print(Fore.RED+Style.BRIGHT+str(61+eoa).rjust(2)+Style.RESET_ALL, end=' - ')
    if myarray[-1]["invested"] != myarray[eoa]["invested"]:
        print(Fore.RED+str(myarray[-1]["invested"] - myarray[eoa]["invested"])+Style.RESET_ALL, end=' - ')
    print('\b\b\b', end='')

def main():
    """monitor various curve contracts"""
    global enter_hit
    load_curvepool_array(carray)
    header_display()
    while True:                                                                     #Initiate main program loop
        month, day, hour, minut = map(str, time.strftime("%m %d %H %M").split())
        firstpass = True                                                            #Prevent header display from outputting in conflict with regular update
        while month+"/"+day+" "+hour+":"+minut == myarray[-1]["human_time"]:        #Wait for each minute to pass to run again
            print(" gas is:", Fore.BLUE+Style.BRIGHT+str(round(w3.eth.gasPrice/10**9)).ljust(3)+Style.RESET_ALL, "  ", "\b"*16, end="", flush=True)
            if enter_hit:
                if firstpass:
                    print("")
                header_display()
            firstpass = False
            time.sleep(6)
            month, day, hour, minut = map(str, time.strftime("%m %d %H %M").split())
        mydict = {"raw_time" : round(time.time()), "human_time": month+"/"+day+" "+hour+":"+minut,
                  "USD" : update_price(), "invested" : sum(carray["invested"])}     #Update dictionary values and price information
        for i in range(0, len(carray["name"])):
            mydict[carray["name"][i]+"invested"] = carray["invested"][i]
            if carray["currentboost"][i] > 0: #sometimes synthetix minter goes into maintenace so we pull last hours values
                try:
                    carray["raw"][i] = call_me(w3.eth.contract(carray["address"][i], abi=abiguage).functions.claimable_tokens(MY_WALLET_ADDRESS))
                    if abs(round(round((carray["raw"][i]+carray["minted"][i])/10**18, 6), 5) - myarray[-1][carray["name"][i]+"pool"]) > 10:
                        print("MINTING HAPPENED: Before", carray["minted"][i], end='   ')
                        carray["minted"][i] = call_me(w3.eth.contract(MINTER_ADDRESS, abi=abiminter).functions.minted(MY_WALLET_ADDRESS, carray["address"][i]))
                        print("After", carray["minted"][i])
                    mydict[carray["name"][i]+"pool"] = round(round((carray["raw"][i]+carray["minted"][i])/10**18, 6), 5)
                    if myarray[-1][carray["name"][i]+"pool"] - mydict[carray["name"][i]+"pool"] > 0.01: #debug lines ... should not happen
                        print(myarray[-1][carray["name"][i]+"pool"] - mydict[carray["name"][i]+"pool"], "\nerror with lower raw value"+carray["name"][i], myarray[-1][carray["name"][i]+"pool"], mydict[carray["name"][i]+"pool"], end='')
                except: #usually happens when snx is down for maintenance
                    mydict[carray["name"][i]+"pool"] = myarrayh[-1][carray["name"][i]+"pool"]
                    carray["raw"][i] = (myarrayh[-1][carray["name"][i]+"pool"]*10**18) - carray["minted"][i]

        mydict["claim"] = round((sum(carray["raw"])+sum(carray["minted"]))/10**18, 6)
        if minut == "00" and mydict["claim"] > 1:
            myarrayh.append(mydict)                                     #Output dictionary to hour file
            if not args.Readonly:
                json.dump(myarrayh, open(file_nameh, "w"), indent=4)
            time.sleep(3)
            show_me(-1, -2, 1, mydict["USD"], 1, 1, myarrayh) #compare last record with 2nd to last, update price, do NOT end line

        myarray.append(mydict)
        if len(myarray) > 61:
            del myarray[0]
        eoa = 0 - len(myarray)
        if not args.Readonly:
            json.dump(myarray, open(file_name, "w"), indent=4)          #Output dictionary to minute file
        print_status_line(myarray[-1]["USD"], eoa)                      #update information on hats and screen
        extramins = round((myarray[-1]["raw_time"]-myarray[eoa]["raw_time"])/60)+eoa
        try:
            curve_hats_update(round((myarray[-1]["claim"]-myarray[eoa]["claim"])/(60+extramins)*60*myarray[-1]["USD"]*24*365/sum(carray["invested"])*100, 2),
                              format((round((myarray[-1]["claim"]-myarray[eoa]["claim"])/(60+extramins)*60, 4)), '.4f'),
                              carray["booststatus"])
        except:
            pass
if __name__ == "__main__":
    main()
