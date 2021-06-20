#!/usr/bin/env python3
"""curve"""
# pylint: disable=C0103,C0301,W0105,E0401,R0914,C0411,W0702,C0200
import json
import time
import cursor
import threading
import argparse
import urllib.request
from colorama import Back, Fore, Style, init
from hour_log_process import show_me, update_price
import logging
logging.getLogger().disabled = True
from web3 import Web3
import yla_watch
logging.getLogger().disabled = False
try:
    from curve_rainbowhat_functions import curve_hats_update
    print("Raspberry Pi Hats Found!")
except:
    1==1
cursor.hide()
init()

MY_WALLET_ADDRESS = "0x8D82Fef0d77d79e5231AE7BFcFeBA2bAcF127E2B"
INFURA_ID = "6aa1a043a9854eaa9fa68d17f619f326"

abiguage = json.load(open("abi/abi_bfcf.json", 'r'))
abiminter = json.load(open("abi/abi_d061.json", 'r'))
abivoting = json.load(open("abi/abi_5f3b.json", 'r'))
abivirtprice = json.load(open("abi/abi_a540.json", 'r'))
MINTER_ADDRESS = "0xd061D61a4d941c39E5453435B6345Dc261C2fcE0"
veCRV_ADDRESS = "0x5f3b5DfEb7B28CDbD7FAba78963EE202a494e2A2"
CRV_ADDRESS = "0xD533a949740bb3306d119CC777fa900bA034cd52"

#abifulcrum = json.load(open("abi/abi_d172.json", 'r'))
abicream = json.load(open("abi/abi_c7fd.json", 'r'))
abiaave2 = json.load(open("abi/abi_c684.json", 'r'))
abieps = json.load(open("abi/abi_4076.json", 'r'))

file_name = "ghistory.json"
file_nameh = "ghistoryh.json"
myarray = json.load(open(file_name, 'r'))
myarrayh = json.load(open(file_nameh, 'r'))
carray = {"longname": [], "name": [], "invested": [], "currentboost": [], "guageaddress" : [], "swapaddress" : [], "tokenaddress" : []}

csym = Fore.MAGENTA + Style.BRIGHT + "Ç" + Style.RESET_ALL + Fore.CYAN
enter_hit = False

parser = argparse.ArgumentParser()
parser.add_argument("-l", "--Local", help = "Local Node Used", action="store_true")
parser.add_argument("-r", "--Readonly", help = "Don't write output to file", action="store_true")
parser.add_argument("-s", "--Small", help = "Small screen size", action="store_true")
parser.add_argument("-b", "--Hourslookback", type=int, help="Use this many hours when calculating pool APR", default=24)
args = parser.parse_args()

bsc_w3 = Web3(Web3.HTTPProvider('https://bsc-dataseed1.binance.org:443'))
infura_w3 = Web3(Web3.HTTPProvider('https://mainnet.infura.io/v3/'+INFURA_ID))
if args.Local:
    print("Data Source: LOCAL (except gas)")
    w3 = Web3(Web3.HTTPProvider('http://192.168.0.198:8545'))
    print("Local Node Found:",w3.isConnected())

    while True:
        a = w3.eth.syncing
        if a is False:
            print("Local Node Sync: Done")
            break
        print("Local Node has:",a['highestBlock']-a['currentBlock'], "blocks left to catch up")

        time.sleep(60)
else:
    print("Data Source: Infura")
    w3 = infura_w3

def key_capture_thread():
    global enter_hit
    enter_hit = False
    input()
    enter_hit = True

def call_me(function):
    """input filtering"""
    x = function.call()
    if isinstance(x, list):
        x = x[0]
    if 0 < x < 10000:
        print("\n odd output when calling "+str(function),x)
    return x

def show_ellipsis():
    try:
        bsc_call=bsc_w3.eth.contract("0x4076CC26EFeE47825917D0feC3A79d0bB9a6bB5c", abi=abieps).functions.claimableRewards(MY_WALLET_ADDRESS).call()
        print(Fore.MAGENTA+Style.BRIGHT+"Ë"+Style.RESET_ALL+Fore.BLUE+str(format(round(bsc_call[0][1]/10**18,2),'.2f').rjust(5))+Style.RESET_ALL, flush=True, end=' ')
        #print(Fore.BLUE+str(format(round(bsc_call[1][1]/10**18,2),'.2f'))+Fore.WHITE+ "B"+Style.RESET_ALL,end=' - ')
    except:
        print("B", end='')

def show_other_exchanges():
    #iusdc_interest = round(w3.eth.contract("0x32E4c68B3A4a813b710595AebA7f6B7604Ab9c15", abi=abifulcrum).functions.nextSupplyInterestRate(1).call()/10**18, 2)
    crcrv_interest = round(((((w3.eth.contract("0xc7Fd8Dcee4697ceef5a2fd4608a7BD6A94C77480", abi=abicream).functions.supplyRatePerBlock().call()*4*60*24/10**18)+1)**364)-1)*100, 2)
    #crusdc_interest = round(((((w3.eth.contract("0x44fbeBd2F576670a6C33f6Fc0B00aA8c5753b322", abi=abicream).functions.supplyRatePerBlock().call()*4*60*24/10**18)+1)**364)-1)*100, 2)
    aacrv_interest = round(w3.eth.contract("0x7d2768dE32b0b80b7a3454c06BdAc94A69DDc7A9", abi=abiaave2).functions.getReserveData("0xD533a949740bb3306d119CC777fa900bA034cd52").call()[3]/10**25,2)
    print("A"+Fore.BLUE+str(format(aacrv_interest, '4.1f')).rjust(4)+Style.RESET_ALL+"%",
          "C"+Fore.BLUE+str(format(crcrv_interest, '4.1f')).rjust(4)+Style.RESET_ALL+"%", end=' ', flush=True)  #+"C"+str(crusdc_interest)+"% "+Fore.MAGENTA+Style.BRIGHT+"Ç"+str(format(crcrv_interest, '.2f'))+"%"
    if not args.Local:
        try:
            webpage1=urllib.request.urlopen("http://192.168.0.198:4333/https://www.hotbit.io/invest/detail/776")
            time.sleep(6)
            webpage = str(webpage1.read())
            try:
                mypos=webpage.index('%        ')    #webpage.index('T+1  ',200)
                hbcrv_interest = str(format(float(webpage[mypos-5:mypos]), '4.1f')).rjust(4)  #float(webpage[mypos-31:mypos-26])
            except:
                hbcrv_interest = "xx.x"
        except:
            hbcrv_interest = "ww.w"
    else:
        time.sleep(6)
        hbcrv_interest = "--.-"
    print("H"+Fore.BLUE+hbcrv_interest+Style.RESET_ALL+"%", end=' ')

def show_yla(eoa,extramins,minut):
    """yla display"""
    buffer=""
    buffer+=Fore.RED+Style.BRIGHT+"y"+Style.RESET_ALL
    try:
        buffer+=str(format(round((myarray[-1]["yla_value"]-myarray[eoa]["yla_value"])/(60+extramins)*60*24*365/myarray[eoa]["yla_invested"]*100, 2), '.2f')).rjust(5)
    except:
        buffer+="xx.xx"
    try:
        buffer += Style.DIM+Fore.GREEN+str(format(round((myarray[-1]["yla_value"]-myarrayh[-args.Hourslookback-1]["yla_value"])/(args.Hourslookback+float(int(minut)/60))/60*60*24*365/myarray[eoa]["yla_invested"]*100, 2), '.2f')).rjust(4)+Style.RESET_ALL+" "
    except:
        buffer += Style.DIM+Fore.GREEN+"xx.xx "+Style.RESET_ALL
    print(buffer, end=' ')

def load_curvepool_array(barray):
    """prepare iteratable array from json file"""
    with open("curvepools.json", 'r') as thisfile:
        thisarray = json.load(thisfile)

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
            barray["minted"][i] = call_me(w3.eth.contract(MINTER_ADDRESS, abi=abiminter).functions.minted(MY_WALLET_ADDRESS, carray["guageaddress"][i]))
            barray["tokenaddress"].append(thisarray[i]["tokenaddress"])
        except:
            barray["tokenaddress"].append("")
        try:
            a = myarray[-1][carray["name"][i]+"pool"]
        except:
            print(thisarray[i]["longname"], "not found in current history file, adding now.")
            myarray[-1][carray["name"][i]+"pool"] = 0
            myarray[-1][carray["name"][i]+"invested"] = 0
        try:
            barray["token_value_modifyer"][i] = thisarray[i]["token_value_modifyer"]
        except:
            barray["token_value_modifyer"][i] = 1

def header_display():
    """display detailed pool information"""
    virutal_price_sum = 0
    cw = [5, 6, 11, 6, 7, 4, 0, 9, 6, 7, 5]
    CRV_inwallet = round(call_me(w3.eth.contract(CRV_ADDRESS, abi=abivoting).functions.balanceOf(MY_WALLET_ADDRESS))/10**18, 2)
    veCRV_locked = round(call_me(w3.eth.contract(veCRV_ADDRESS, abi=abivoting).functions.locked(MY_WALLET_ADDRESS))/10**18, 2)
    veCRV_mine = round(call_me(w3.eth.contract(veCRV_ADDRESS, abi=abivoting).functions.balanceOf(MY_WALLET_ADDRESS))/10**18, 2)
    veCRV_total = round(call_me(w3.eth.contract(veCRV_ADDRESS, abi=abivoting).functions.totalSupply())/10**18, 2)
    for i in range(0, len(carray["name"])):
        carray["totalsupply"][i] = round(call_me(w3.eth.contract(carray["guageaddress"][i], abi=abiguage).functions.totalSupply())/10**18, 2)
        carray["virtprice"][i] = round(call_me(w3.eth.contract(carray["swapaddress"][i], abi=abivirtprice).functions.get_virtual_price())/10**18, 6)
        carray["balanceof"][i] = round(call_me(w3.eth.contract(carray["guageaddress"][i], abi=abiguage).functions.balanceOf(MY_WALLET_ADDRESS))/10**18, 2)
        if len(carray["tokenaddress"][i]) > 1:
            carray["balanceof"][i] += round(call_me(w3.eth.contract(carray["tokenaddress"][i], abi=abiguage).functions.balanceOf(MY_WALLET_ADDRESS))/10**18, 2)
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

    print("$"+str(sum(carray["invested"])), "invested, is now",int(virutal_price_sum), end=' ')
    print("("+str(format(round(( virutal_price_sum/sum(carray["invested"])*100)-100,5),'.3f'))+"%)", end='   ')
    print("Ç"+str(round(veCRV_locked)), "veCRV locked" +Style.DIM+" ("+str(veCRV_mine), "voting)"+Style.RESET_ALL, end='   ')
    print(csym+str(round(myarray[-1]["claim"]-(sum(carray["minted"])/10**18), 2))+Style.RESET_ALL, "in pools", end=' ')
    #print(csym+str(round(sum(carray["minted"])/10**18, 2))+Style.RESET_ALL, "minted", end=' ')
    print("("+csym+str(CRV_inwallet)+Style.RESET_ALL,"on sidelines)", end='  ')

    eoa = 0 - len(myarray)
    if round((round(time.time())-myarray[eoa]["raw_time"])/60, 2)+eoa >= 0.5:
        print(Fore.RED+str(round(((round(time.time())-myarray[eoa]["raw_time"])/60)+eoa, 2))+Style.RESET_ALL+" min oos.", end=' ')
    if eoa > -61:
        print(Fore.RED+str(61+eoa)+Style.RESET_ALL+" minutes under 60.", end=' ')
    if sum(carray["invested"]) != myarray[eoa]["invested"]:
        print(Fore.RED+str(sum(carray["invested"]) - myarray[eoa]["invested"])+Style.RESET_ALL+" of New $ obs. data", end='')
    print("")
    threading.Thread(target=key_capture_thread, args=(), name='key_capture_thread', daemon=True).start()

def boost_check():
    """update variables to check boost status"""
    veCRV_mine = round(call_me(w3.eth.contract(veCRV_ADDRESS, abi=abivoting).functions.balanceOf(MY_WALLET_ADDRESS))/10**18, 2)
    veCRV_total = round(call_me(w3.eth.contract(veCRV_ADDRESS, abi=abivoting).functions.totalSupply())/10**18, 2)
    outputflag = 0
    for i in range(0, len(carray["name"])):
        if carray["currentboost"][i] >= 2.47:   #hack to avoid spool which is annoyingly close to 2.5 boost
            carray["booststatus"][i] = -1               #Green, all is well
        elif carray["currentboost"][i] == 0:
            carray["booststatus"][i] = 4                #Blue, pool is empty
        else:
            carray["balanceof"][i] = round(call_me(w3.eth.contract(carray["guageaddress"][i], abi=abiguage).functions.balanceOf(MY_WALLET_ADDRESS))/10**18, 2)
            carray["totalsupply"][i] = round(call_me(w3.eth.contract(carray["guageaddress"][i], abi=abiguage).functions.totalSupply())/10**18, 2)
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

def print_status_line(USD, eoa):
    """print main status line"""
    extramins = round((myarray[-1]["raw_time"]-myarray[eoa]["raw_time"])/60)+eoa
    difference = (myarray[-1]["claim"]-myarray[eoa]["claim"])/(60+extramins)*60
    if args.Small:
        print("\033[A"*3,end='')
    print("\r",end='',flush=True)
    print(myarray[-1]["human_time"], end=' ')
    print("$"+Fore.YELLOW+Style.BRIGHT+str(format(USD, '.2f'))+Style.RESET_ALL, end = ' - ') #csym+"1"+Style.RESET_ALL+" = "+
    tprofit = 0
    buffer = ""
    month, day, hour, minut = map(str, time.strftime("%m %d %H %M").split())
    for i in range(0, len(carray["name"])):
        if carray["currentboost"][i] > 0:
            buffer+=Fore.RED+Style.BRIGHT+carray["name"][i]+Style.RESET_ALL
            try:
                buffer+=str(format(round((myarray[-1][carray["name"][i]+"pool"]-myarray[eoa][carray["name"][i]+"pool"])/(60+extramins)*60*USD*24*365/carray["invested"][i]*100, 2), '.2f')).rjust(5)
            except:
                buffer+="xx.xx"
            try:
                tprofit += (myarray[-1][carray["name"][i]+"profit"]-myarrayh[-args.Hourslookback-1][carray["name"][i]+"profit"])/(args.Hourslookback+float(int(minut)/60))
                buffer += Style.DIM+Fore.GREEN+str(format(round((myarray[-1][carray["name"][i]+"profit"]-myarrayh[-args.Hourslookback-1][carray["name"][i]+"profit"])/(args.Hourslookback+float(int(minut)/60))/60*60*USD*24*365/carray["invested"][i]*100, 2), '.2f')).rjust(4)+Style.RESET_ALL+" "
            except:
                buffer += Style.DIM+Fore.GREEN+"xx.xx "+Style.RESET_ALL

    print(Fore.GREEN+Style.BRIGHT+str(format(round((difference)*USD*24*365/sum(carray["invested"])*100, 2), '.2f'))+Style.RESET_ALL+"/", end='')
    #print(Fore.CYAN+str(format(round((difference)*24*365/sum(carray["invested"])*100, 2), '.2f')).rjust(5)+Fore.WHITE+"% APR", end='')
    print(Fore.YELLOW+str(format(round((tprofit/60*60)*24*365/sum(carray["invested"])*100, 2), '.2f'))+Style.RESET_ALL+"% APR", end='')
    if args.Small:
        print("\n"+buffer)
    else:
        print(' -',buffer+'- ', end='')
    #print("H"+csym+format((round(difference, 5)), '.4f')+Style.RESET_ALL, end=' ')
    print("D"+csym+format((round(difference*24, 2)), '.2f').rjust(5)+Style.RESET_ALL+
          "/$"+Fore.YELLOW+str(format(round(24*tprofit,2), '.2f'))+Style.RESET_ALL,
          "Y"+csym+format((round(difference*24*365, 0)), '.0f').rjust(4)+Style.RESET_ALL+
          "/$"+Fore.YELLOW+str(format(round(24*365*tprofit,2), '.0f')).rjust(3)+Style.RESET_ALL, end=' ')
    #show_additional_pool_coins()
    boost_check()
    if args.Small:
        print("")
    else:
        print('- ', end='')
    show_other_exchanges()
    #show_ellipsis()
    show_yla(eoa,extramins,minut)
    if extramins >= 0: #air bubble extra minutes
        print(Fore.RED+str(round((myarray[-1]["raw_time"]-myarray[eoa]["raw_time"])/60)+eoa+1)+Style.RESET_ALL, end=' ', flush=True)
    if eoa > -61:  #fewer than 60 records in the ghistory.json file
        print(Fore.RED+Style.BRIGHT+str(61+eoa).rjust(2)+Style.RESET_ALL, end=' ', flush=True)
    if myarray[-1]["invested"] != myarray[eoa]["invested"]:
        print(Fore.RED+str(myarray[-1]["invested"] - myarray[eoa]["invested"])+Style.RESET_ALL, end=' ', flush=True)

    return round(((difference*myarray[-1]["USD"])+(tprofit/60*60))*24*365/sum(carray["invested"])*100, 2) #display_percent

def main():
    """monitor various curve contracts"""
    load_curvepool_array(carray)
    print("Calc Pool APR over hours:",args.Hourslookback)
    print("Read Only Mode:",args.Readonly)
    if not args.Small:
        header_display()
    else:
        print("\n"*3)
    while True:                                                                     #Initiate main program loop
        month, day, hour, minut = map(str, time.strftime("%m %d %H %M").split())
        firstpass = True                                                            #Prevent header display from outputting in conflict with regular update
        while month+"/"+day+" "+hour+":"+minut == myarray[-1]["human_time"]:        #Wait for each minute to pass to run again
            try:
                print(str("~"+str(round(infura_w3.eth.gasPrice/10**9))+"~").rjust(5), "\b"*6, end="", flush=True)
            except:
                print(str("~"+Fore.RED+Style.BRIGHT+"xxx"+Style.RESET_ALL+"~"), "\b"*6, end="", flush=True)
            if firstpass and minut == "00":
                print("")
                if args.Small:
                    print("\n"*3)
            if enter_hit:
                if firstpass:
                    print("")
                header_display()
            firstpass = False
            time.sleep(6)
            month, day, hour, minut = map(str, time.strftime("%m %d %H %M").split())
        mydict = {"raw_time" : round(time.time()), "human_time": month+"/"+day+" "+hour+":"+minut,
                  "USD" : update_price("curve-dao-token"), "invested" : sum(carray["invested"])}     #Update dictionary values and price information
        for i in range(0, len(carray["name"])):
            mydict[carray["name"][i]+"invested"] = carray["invested"][i]
            try:
                if carray["raw"][i] > 0: #skip updating empty pools after the initial check
                    carray["raw"][i] = call_me(w3.eth.contract(carray["guageaddress"][i], abi=abiguage).functions.claimable_tokens(MY_WALLET_ADDRESS))
                    carray["virtprice"][i] = call_me(w3.eth.contract(carray["swapaddress"][i], abi=abivirtprice).functions.get_virtual_price())/10**18
                    carray["balanceof"][i] = call_me(w3.eth.contract(carray["guageaddress"][i], abi=abiguage).functions.balanceOf(MY_WALLET_ADDRESS))/10**18
                    if (carray["virtprice"][i]*carray["balanceof"][i]*carray["token_value_modifyer"][i])-carray["invested"][i] > -10:
                        mydict[carray["name"][i]+"profit"] = (carray["virtprice"][i]*carray["balanceof"][i]*carray["token_value_modifyer"][i])-carray["invested"][i]
                if abs(round((carray["raw"][i]+carray["minted"][i])/10**18, 5) - myarray[-1][carray["name"][i]+"pool"]) > 3:
                    print("\nMINTING HAPPENED:", carray["name"][i], "pool      Before", carray["minted"][i], end='   ')
                    carray["minted"][i] = call_me(w3.eth.contract(MINTER_ADDRESS, abi=abiminter).functions.minted(MY_WALLET_ADDRESS, carray["guageaddress"][i]))
                    print("After", carray["minted"][i])
                mydict[carray["name"][i]+"pool"] = round((carray["raw"][i]+carray["minted"][i])/10**18, 5)
                if myarray[-1][carray["name"][i]+"pool"] - mydict[carray["name"][i]+"pool"] > 0.01: #debug lines ... should not happen
                    print(myarray[-1][carray["name"][i]+"pool"] - mydict[carray["name"][i]+"pool"], "\nerror with lower raw value"+carray["name"][i], myarray[-1][carray["name"][i]+"pool"], mydict[carray["name"][i]+"pool"], end='')
            except: #usually happens when snx is down for maintenance
                mydict[carray["name"][i]+"pool"] = myarrayh[-1][carray["name"][i]+"pool"]
                carray["raw"][i] = (myarrayh[-1][carray["name"][i]+"pool"]*10**18) - carray["minted"][i]
        mydict["yla_value"] = yla_watch.yla_getvalue(False)
        mydict["yla_invested"] = 7150
        mydict["claim"] = round((sum(carray["raw"])+sum(carray["minted"]))/10**18, 6)
        if minut == "00" and mydict["claim"] > 1:
            myarrayh.append(mydict)                                     #Output dictionary to hour file
            if not args.Readonly:
                print(Fore.RED+Style.BRIGHT+"Write", flush=True, end='')
                json.dump(myarrayh, open(file_nameh, "w"), indent=4)
                print("\b\b\b\b\b"+Style.RESET_ALL+"Done!", flush=True, end='')
            time.sleep(3)
            #show_me(-1, -2, 1, mydict["USD"], 1, 1, myarrayh) #compare last record with 2nd to last, update price, do NOT end line

        myarray.append(mydict)
        if len(myarray) > 61:
            del myarray[0]
        eoa = 0 - len(myarray)
        if not args.Readonly:
            json.dump(myarray, open(file_name, "w"), indent=4)          #Output dictionary to minute file
        display_percent = print_status_line(myarray[-1]["USD"], eoa)    #update information on hats and screen
        try:
            curve_hats_update(display_percent,
                              str(format(round(update_price("ethereum")),',')).rjust(6),
                              carray["booststatus"])
        except:
            pass
if __name__ == "__main__":
    main()
