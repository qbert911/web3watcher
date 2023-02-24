#!/usr/bin/env python3
"""curve"""

# pylint: disable=C0103,C0301,W0105,E0401,R0914,C0411,W0702,C0200,C0116,w0106
import cursor
import threading
import shutil
import argparse
import json
import time
import random
import requests
from web3 import Web3
from colorama import Fore, Style, init
from tools.curve_rainbowhat_functions import curve_hats_update
from tools.price_getter import update_price, update_price2
from tools.load_contract import load_contract
import convex_examiner
import curve_functions
import status_line_printer
import header_printer

cursor.hide()                               #don't draw the cursor
init()                                      #initialize colorama

#INFURA_ID = "1d651358519346beb661128bf65ab651"
INFURA_ID = "bfdd3973b810492db7cb27792702782f"

infura_w3 = Web3(Web3.HTTPProvider(f'https://mainnet.infura.io/v3/{INFURA_ID}'))
mylocal_w3 = Web3(Web3.HTTPProvider('http://192.168.0.146:8545'))
mylocal_w3 = Web3(Web3.HTTPProvider('http://192.168.0.4:8545'))
#mylocal_w3 = Web3(Web3.WebsocketProvider("ws://192.168.0.146:8546"))

file_name = "ghistory.json"
file_nameh = "ghistoryh.json"
myarray = json.load(open(file_name, 'r'))
myarrayh = json.load(open(file_nameh, 'r'))
carray = {"longname": [], "name": [], "invested": [], "currentboost": [], "gaugeaddress" : [], "swapaddress" : [], "tokenaddress" : []}

enter_hit = False

parser = argparse.ArgumentParser()
parser.add_argument("-f", "--Fullheader", help = "Show empty pools in header", action="store_true")
parser.add_argument("-l", "--Local", help = "Local Node Used", action="store_true")
parser.add_argument("-r", "--Readonly", help = "Don't write output to file", action="store_true")
parser.add_argument("-b", "--Hourslookback", type=int, help="Use this many hours when calculating pool APR", default=24)
parser.add_argument("-o", "--Outputtohats", help = "Raspberry Pi Hats Signaling", action="store_true")
args = parser.parse_args()

def wait_for_local_node_sync(w3,waitforit=False):
    while True:
        try:
            a = w3.eth.syncing
            try:
                blockdiff = a['highestBlock']-a['currentBlock']
            except Exception:
                blockdiff = 0
            if a is False or blockdiff < 15:
                break
            print("\rLocal Node has:",blockdiff, "blocks left to catch up\r", end="")
            if not waitforit:
                return False
            time.sleep(10)
        except Exception:
            print("\r\x1b[20C Local Node communication error   !!!switching to infura!!!")
            return False
    return True

def key_capture_thread():
    global enter_hit
    enter_hit = False
    input()
    enter_hit = True

def pyportal_update(mydict, display_percent, dollar_amount, crv_daily, cvx_daily):
    # sourcery skip: merge-dict-assign
    pyportal_dict = {}
    pyportal_dict["display_percent"] = display_percent
    pyportal_dict["price_string"] = f"{mydict['FRAX']:.1f}"+f"{mydict['SPELL']*10000:.0f}".rjust(3)
    pyportal_dict["dollar_amount"] = dollar_amount
    pyportal_dict["crv_daily"] = crv_daily
    pyportal_dict["cvx_daily"] = cvx_daily
    pyportal_dict["ethbtcratio"] = f"{mydict['ETH']/mydict['BTC'] * 1000: 3.0f}"
    pyportal_dict["cvxcrvratio"] = f"{mydict['USDcvx']/mydict['USD'] * 100:03.0f}"
    pyportal_dict["crvcvxratio"] = f"{mydict['USD']/mydict['USDcvx'] * 1000:03.0f}"

    try:
        json.dump(pyportal_dict, open("pyportal.json", "w"), indent=4)
    except Exception:
        print("error writing to pyportal.json")

def show_headers(w3):
    #curve_functions.curve_header_display(myarray, carray, w3, args.Fullheader)
    #header_printer.stakedao_header_display(myarray, myarrayh, args.Hourslookback)
    header_printer.curve_header_display2(myarray, carray, w3, args.Fullheader, myarrayh, args.Hourslookback)
    header_printer.abracadabra_header_display(myarray, myarrayh, args.Hourslookback)
    header_printer.conic_header_display(myarray, myarrayh, args.Hourslookback)
    header_printer.clev_header_display(myarray,myarrayh,args.Hourslookback)
    header_printer.concentrator_locked_header_display(myarray,myarrayh,args.Hourslookback)
    header_printer.concentrator_header_display(myarray,myarrayh,args.Hourslookback)
    header_printer.convex_header_display(myarray, myarrayh, args.Hourslookback)
    header_printer.combined_stats_display(myarray, carray, w3)
    threading.Thread(target=key_capture_thread, args=(), name='key_capture_thread', daemon=True).start()

def get_chainlink_price(contract_address, w3):
    try:
        contract = load_contract(contract_address, w3)
        value = contract.latestAnswer().call() / 10**8 #contract.decimals().call()
    except Exception:
        value = 0
    return value   

def gas_and_sleep(w3, mydict):
    pass_count = 1    #Prevent header display from outputting in conflict with regular update
    month, day, hour, minut = map(str, time.strftime("%m %d %H %M").split())

    mydict["FRAX"] = get_chainlink_price('0x6Ebc52C8C1089be9eB3945C4350B68B8E4C2233f',w3)
    mydict["SPELL"] = get_chainlink_price('0x8c110B94C5f1d347fAcF5E1E938AB2db60E3c9a8',w3)
    mydict["ETH"] = get_chainlink_price('0x5f4eC3Df9cbd43714FE2740f5E3616155c5b8419',w3)
    mydict["BTC"] = get_chainlink_price('0xF4030086522a5bEEa4988F8cA5B36dbC97BeE88c',w3)
    mydict["USDcvx"] = get_chainlink_price('0xd962fC30A72A84cE50161031391756Bf2876Af5D',w3)
    mydict["USD3pool"] = 1.021

    #mydict["USD"] = get_chainlink_price('0xCd627aA160A6fA45Eb793D19Ef54f5062F20f33f',w3)
    mydict["USD"] = update_price("curve-dao-token",'▹','▸',myarray[-1]["USD"])
    mydict["USDcvxCRV"] = update_price("convex-crv",'▹','▸',myarray[-1]["USDcvxCRV"])

    mydict["CTR"] = myarray[-1]["CTR"]
    mydict["USDcvxCLEV"] = myarray[-1]["USDcvxCLEV"]
    mydict["CLEV"] = myarray[-1]["CLEV"]
    mydict["CNC"] = myarray[-1]["CNC"]

    if random.getrandbits(1):
        mydict["CTR"] = update_price("concentrator",'▹','1',myarray[-1]["CTR"])
    elif random.getrandbits(1):
        mydict["CNC"] = update_price("conic-finance",'▹','2',myarray[-1]["CNC"])
    elif random.getrandbits(1):
        mydict["CLEV"] = update_price("clever-token",'▹','3',myarray[-1]["CLEV"])
    else:
        mydict["USDcvxCLEV"] = update_price("clever-cvx",'▹','4',myarray[-1]["USDcvxCLEV"]) #abccvx not on cg yet?



    month, day, hour, minut = map(str, time.strftime("%m %d %H %M").split())
    while f"{month}/{day} {hour}:{minut}" == myarray[-1]["human_time"]:#Wait for each minute to pass to run again
        try:
            #print(pass_count,end='', flush=True)
            print(f"~{round(w3.eth.gas_price / 10**9)}~"[:5].rjust(5),pass_count, "\b" * 8, end="", flush=True)
        except Exception:
            print(f"~{Fore.RED}{Style.BRIGHT}xxx{Style.RESET_ALL}~", "\b" * 6, end="", flush=True)
        if pass_count == 1 and minut == "00":
            print("")
        if enter_hit:
            if pass_count == 1:
                print("")
            show_headers(w3)
        pass_count += 1
        time.sleep(10)
        month, day, hour, minut = map(str, time.strftime("%m %d %H %M").split())
    if args.Local and not wait_for_local_node_sync(w3):
            w3 = infura_w3
    print("\r",end="")
    return w3

def main():
    """monitor various curve contracts"""
    print("Calc Pool APR over hours:",args.Hourslookback)
    print("Read Only Mode:",args.Readonly)
    print("Output to Hats:",args.Outputtohats)
    if not args.Local:
        print("Data Source: Infura")
        w3 = infura_w3
    else:
        print("Data Source: LOCAL")
        w3 = mylocal_w3
        if not wait_for_local_node_sync(w3,waitforit=True):
            w3 = infura_w3
    constants={}
    curve_functions.load_curvepools_fromjson(myarray, carray, w3)
    show_headers(w3)
#Main program loop starts here
    while True:
#Check gas price every 10 seconds and wait for a minute to pass
        mydict = {}
        w3 = gas_and_sleep(w3, mydict)
#Update dictionary values and price information
        month, day, hour, minut = map(str, time.strftime("%m %d %H %M").split())
        mydict["raw_time"] = round(time.time())
        mydict["human_time"] = f"{month}/{day} {hour}:{minut}"
        mydict["invested"] = sum(carray["invested"])

        curve_functions.update_curve_pools(mydict, carray, myarray, myarrayh, w3)

        mydict["cvxlocked_rewards"] = convex_examiner.cvxlocked_getvalue(myarray, w3, "0x72a19342e8F1838460eBFCCEf09F6585e32db86E")
        mydict["crvstaked_rewards"] = convex_examiner.crvstaked_getvalue(myarray, w3, "0xaa0C3f5F7DFD688C6E646F66CD2a6B66ACdbE434")
        
        mydict["crvsquared_rewards"], constants = convex_examiner.regx_getvalue(myarray, w3, "crvsquared_rewards", constants, poolid=41)
        try:
            balances = load_contract("0x9D0464996170c6B9e75eED71c68B99dDEDf279e8", w3).get_balances().call() 
            mydict["crvsquared_balances"] = balances[0]/(balances[0]+balances[1])
        except Exception:
            mydict["crvsquared_balances"] = 0

        mydict["cvxeth_rewards"] = myarray[-1]["cvxeth_rewards"] #, constants = convex_examiner.regx_getvalue(myarray, w3, "cvxeth_rewards", constants, poolid=64)
        mydict["spelleth_rewards"] = myarray[-1]["spelleth_rewards"] #, constants = convex_examiner.regx_getvalue(myarray, w3, "spelleth_rewards", constants, poolid=66)
        #mydict["fxslocked_rewards"], constants = convex_examiner.regx_getvalue(myarray, w3, "fxslocked_rewards", constants, poolid=72)

        try:
            mydict["fxslocked_oracle"] = load_contract("0xd658A338613198204DCa1143Ac3F01A722b5d94A", w3).price_oracle().call() / 10**18
        except Exception:
            mydict["fxslocked_oracle"] = 0
        mydict["concentrator_cvxeth_rewards"], constants = convex_examiner.regx_getvalue(myarray, w3, "concentrator_cvxeth_rewards", constants, poolid=64, wallet_address="0x3Cf54F3A1969be9916DAD548f3C084331C4450b5")
        mydict["concentrator_rewards_CTR"], mydict["concentrator_virt"], mydict["concentrator_x2e_virt"], \
        mydict["concentrator_ve_current"], mydict["concentrator_ve_locked"], mydict["concentrator_ve_claimable"] = convex_examiner.concentrator_getvalues(myarray, w3)

        mydict["abra_spelleth"], constants = convex_examiner.abracadabra_getvalue(myarray, w3, "abra_spelleth", "0xF43480afE9863da4AcBD4419A47D9Cc7d25A647F", constants,0)
        #mydict["stakedao_crvstaked"] = convex_examiner.stakedao_getvalue(myarray, w3, "stakedao_crvstaked", "0x7f50786A0b15723D741727882ee99a0BF34e3466",0)


        MY_WALLET_ADDRESS = "0x8D82Fef0d77d79e5231AE7BFcFeBA2bAcF127E2B" #hacky
        try:
            contract = load_contract("0xC67e9Cdf599369130DD0841Ee5CB8eBF9BB661C4", w3)
            mydict["cnceth_balance"] = contract.balances(MY_WALLET_ADDRESS).call() / 10**18
            mydict["cnceth_rewards"] = contract.claimableRewards(MY_WALLET_ADDRESS).call() / 10**18
        except Exception:
            mydict["cnceth_balance"] = 0
            mydict["cnceth_rewards"] = 0

        mydict["cnceth_concentrator_rewards"], constants = convex_examiner.regx_getvalue(myarray, w3, "crvsquared_rewards", constants, poolid=152)

        try:
            contract = load_contract("0x5BC3dD6E6b4E5DD811d558843DA6A1bfBB9c9dCa", w3)
            mydict["ctreth_balance"] = contract.balanceOf(MY_WALLET_ADDRESS).call() / 10**18
            mydict["ctreth_rewards"] = contract.claimable_reward(MY_WALLET_ADDRESS,"0x2b95A1Dcc3D405535f9ed33c219ab38E8d7e0884").call() / 10**18
        except Exception:
            mydict["ctreth_balance"] = 0
            mydict["ctr_rewards"] = 0

        try:
            contract = load_contract("0xc5022291cA8281745d173bB855DCd34dda67F2f0", infura_w3)
            mydict["abcCVX_balance"] = contract.balanceOf(MY_WALLET_ADDRESS).call()  / 10**18
            mydict["abcCVX_rewards"] = contract.claimable_tokens(MY_WALLET_ADDRESS).call()  / 10**18
            a = requests.get("https://api.curve.fi/api/getPools/ethereum/factory",timeout=20)
            mydict["abcCVX_baseapy"] = a.json()['data']['poolData'][209]['gaugeCrvApy'][0]*1.82 #this grabs the lower end apy value from factory pool 209 clevCVX-f
        except Exception:
            mydict["abcCVX_balance"] = 0
            mydict["abcCVX_rewards"] = 0
            mydict["abcCVX_baseapy"] = 0

        contract = load_contract("0xDAF03D70Fe637b91bA6E521A32E1Fb39256d3EC9", w3,abi_address="0xeb5EB007Ab39e9831a1921E8116Bc353AFE5BA2C")
        mydict["afxs_balance"] = contract.balanceOf(MY_WALLET_ADDRESS).call() / 10**18
        mydict["afxs_totalsupply"] = contract.totalSupply().call() / 10**18
        mydict["afxs_virt"] = float(contract.totalAssets().call() / (mydict["afxs_totalsupply"] * 10**18))
        mydict["fxslocked_rewards"], constants = convex_examiner.regx_getvalue(myarray, w3, "fxslocked_rewards", constants, poolid=72, wallet_address="0xDAF03D70Fe637b91bA6E521A32E1Fb39256d3EC9",mypoolportion=mydict["afxs_balance"]/mydict["afxs_totalsupply"])


        #when cvx/eth harvests to acrv pile ...
        if mydict["concentrator_rewards_CTR"] > myarray[-1]["concentrator_rewards_CTR"]:
            print("")
#Keep one hour worth of data in hourly log
        myarray.append(mydict)
        while len(myarray) > 61:
            del myarray[0]
#Output dictionary to minute file
        if not args.Readonly:
            shutil.copyfile(file_name, f"{file_name}.bak")
            json.dump(myarray, open(file_name, "w"), indent=4)            
#Output dictionary to hour file on the top of each hour
        if minut == "00" and mydict["claim"] > 1:
            myarrayh.append(mydict)
            if not args.Readonly:
                shutil.copyfile(file_nameh, f"{file_nameh}.bak")
                json.dump(myarrayh, open(file_nameh, "w"), indent=4)
#update information on screen and pi hats when possible
        dollar_amount, mainpercentdisplay,crv_daily,cvx_daily = status_line_printer.print_status_line(carray, myarray, myarrayh, 0 - len(myarray), w3, args.Hourslookback)
        pyportal_update(mydict, mainpercentdisplay, dollar_amount,crv_daily,cvx_daily)
        if args.Outputtohats:
            try:
                curve_hats_update(mainpercentdisplay, carray["booststatus"], mydict["ETH"])
            except Exception:
                pass

if __name__ == "__main__":
    main()
