#!/usr/bin/env python3
"""curve"""
# pylint: disable=C0103,C0301,W0105,E0401,R0914,C0411,W0702,C0200,C0116,w0106
import cursor
import threading
import shutil
import argparse
import json
import time
from web3 import Web3
from colorama import Fore, Style, init
from tools.curve_rainbowhat_functions import curve_hats_update
from tools.price_getter import update_price
from tools.load_contract import load_contract
import convex_examiner
import curve_functions
import status_line_printer
import header_printer

cursor.hide()                               #don't draw the cursor
init()                                      #initialize colorama

INFURA_ID = "9c51dd19cb9e456387014e7d1661afa3"

infura_w3 = Web3(Web3.HTTPProvider('https://mainnet.infura.io/v3/'+INFURA_ID))
mylocal_w3 = Web3(Web3.HTTPProvider('http://192.168.0.146:8545'))
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
            print("\rLocal Node communication error   !!!switching to infura!!!")
            return False
    return True

def key_capture_thread():
    global enter_hit
    enter_hit = False
    input()
    enter_hit = True

def pyportal_update(mydict, display_percent, dollar_amount, crv_daily, cvx_daily):
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
    header_printer.curve_header_display2(myarray, carray, w3, args.Fullheader, myarrayh, args.Hourslookback)
    header_printer.convex_header_display(myarray, myarrayh, args.Hourslookback)
    header_printer.combined_stats_display(myarray, carray, w3)
    threading.Thread(target=key_capture_thread, args=(), name='key_capture_thread', daemon=True).start()

def get_chainlink_price(contract_address, w3):
    contract = load_contract(contract_address, w3)
    return contract.latestAnswer().call() / 10**contract.decimals().call()

def gas_and_sleep(w3, mydict):
    firstpass = True    #Prevent header display from outputting in conflict with regular update
    month, day, hour, minut = map(str, time.strftime("%m %d %H %M").split())

    mydict["FRAX"] = get_chainlink_price('0x6Ebc52C8C1089be9eB3945C4350B68B8E4C2233f',w3)
    mydict["SPELL"] = get_chainlink_price('0x8c110B94C5f1d347fAcF5E1E938AB2db60E3c9a8',w3)
    mydict["ETH"] = get_chainlink_price('0x5f4eC3Df9cbd43714FE2740f5E3616155c5b8419',w3)
    mydict["BTC"] = get_chainlink_price('0xF4030086522a5bEEa4988F8cA5B36dbC97BeE88c',w3)
    mydict["USDcvx"] = get_chainlink_price('0xd962fC30A72A84cE50161031391756Bf2876Af5D',w3)
    mydict["USD3pool"] = 1.021

    #mydict["USD"] = get_chainlink_price('0xCd627aA160A6fA45Eb793D19Ef54f5062F20f33f',w3)
    mydict["USD"] = update_price("curve-dao-token",'▸','▹',myarray[-1]["USD"])
    mydict["USDcvxCRV"] = update_price("convex-crv",'▸','▹',myarray[-1]["USDcvxCRV"])

    month, day, hour, minut = map(str, time.strftime("%m %d %H %M").split())
    while month+"/"+day+" "+hour+":"+minut == myarray[-1]["human_time"]:        #Wait for each minute to pass to run again
        try:
            print(str("~"+str(round(infura_w3.eth.gasPrice/10**9))+"~")[0:5].rjust(5),"\b"*6, end="", flush=True)
        except Exception:
            print(str("~"+Fore.RED+Style.BRIGHT+"xxx"+Style.RESET_ALL+"~"), "\b"*6, end="", flush=True)
        if firstpass and minut == "00":
            print("")
        if enter_hit:
            if firstpass:
                print("")
            show_headers(w3)
        firstpass = False
        time.sleep(10)
        month, day, hour, minut = map(str, time.strftime("%m %d %H %M").split())
    if args.Local:
        if not wait_for_local_node_sync(w3):
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
        print("Data Source: LOCAL (except gas)")
        w3 = mylocal_w3
        if not wait_for_local_node_sync(w3,waitforit=True):
            w3 = infura_w3
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
        mydict["human_time"] = month+"/"+day+" "+hour+":"+minut
        mydict["invested"] = sum(carray["invested"])

        curve_functions.update_curve_pools(mydict, carray, myarray, myarrayh, w3)

        mydict["crvstaked_rewards"] = convex_examiner.crvstaked_getvalue(myarray, w3, "0x3Fe65692bfCD0e6CF84cB1E7d24108E434A7587e")
        mydict["cvxlocked_rewards"] = convex_examiner.cvxlocked_getvalue(myarray, w3, "0x72a19342e8F1838460eBFCCEf09F6585e32db86E")

        #mydict["trix_rewards"] = convex_examiner.regx_getvalue(myarray, w3, "trix_rewards", "0x9D5C5E364D81DaB193b72db9E9BE9D8ee669B652")
        #mydict["mimx_rewards"] = convex_examiner.regx_getvalue(myarray, w3, "mimx_rewards", "0xC62DE533ea77D46f3172516aB6b1000dAf577E89")
        #mydict["crveth_rewards"] = convex_examiner.regx_getvalue(myarray, w3, "crveth_rewards", "0x085A2054c51eA5c91dbF7f90d65e728c0f2A270f")
        mydict["cvxeth_rewards"] = convex_examiner.regx_getvalue(myarray, w3, "cvxeth_rewards", "0xb1Fb0BA0676A1fFA83882c7F4805408bA232C1fA")
        mydict["spelleth_rewards"] = convex_examiner.regx_getvalue(myarray, w3, "spelleth_rewards", "0xb2f0bB6352417c1Bf017862aC165E67623611aF3")
        mydict["fxslocked_rewards"] = convex_examiner.regx_getvalue(myarray, w3, "fxslocked_rewards", "0xf27AFAD0142393e4b3E5510aBc5fe3743Ad669Cb")
        mydict["crvsquared_rewards"] = convex_examiner.regx_getvalue(myarray, w3, "crvsquared", "0x0392321e86F42C2F94FBb0c6853052487db521F0")

        #mydict["crveth_virt"] = convex_examiner.virt_grabber(myarray, w3, "crveth_virt", "0x8301AE4fc9c624d1D396cbDAa1ed877821D7C511")
        mydict["cvxeth_virt"] = convex_examiner.virt_grabber(myarray, w3, "cvxeth_virt", "0xB576491F1E6e5E62f1d8F26062Ee822B40B0E0d4")
        mydict["spelleth_virt"] = convex_examiner.virt_grabber(myarray, w3, "spelleth_virt", "0x98638FAcf9a3865cd033F36548713183f6996122")
        mydict["fxslocked_virt"] = convex_examiner.virt_grabber(myarray, w3, "fxslocked_virt", "0xd658A338613198204DCa1143Ac3F01A722b5d94A")
        mydict["crvsquared_virt"] = convex_examiner.virt_grabber(myarray, w3, "crvsquared_virt", "0x9D0464996170c6B9e75eED71c68B99dDEDf279e8")

        mydict["fxslocked_oracle"] = convex_examiner.oracle_grabber(myarray, w3, "fxslocked_oracle", "0xd658A338613198204DCa1143Ac3F01A722b5d94A")

        mydict["fxslocked_extracvx"] = convex_examiner.earned_grabber(myarray, w3,"fxslocked_extracvx ","0xE2585F27bf5aaB7756f626D6444eD5Fc9154e606")
        mydict["fxslocked_extrafxs"] = convex_examiner.earned_grabber(myarray, w3,"fxslocked_extrafxs","0x28120D9D49dBAeb5E34D6B809b842684C482EF27")    
        mydict["cvxeth_extracvx"] = convex_examiner.earned_grabber(myarray, w3,"cvxeth_extracvx ","0x834B9147Fd23bF131644aBC6e557Daf99C5cDa15")
        mydict["crvsquared_extracvx"] = convex_examiner.earned_grabber(myarray, w3,"crvsquared_extracvx ","0xbE4DEa8E5d1E53FAd661610E47501f858F25852D")

        concentrator = load_contract("0x3Cf54F3A1969be9916DAD548f3C084331C4450b5",w3,"0x99373AE646ed89b9A466c4256b09b10dbCC07B40")
        mydict["concentrator_totalmined"] = concentrator.ctrMined().call()/10**18
        mydict["concentrator_rewards_CTR"] = concentrator.pendingCTR(5,"0x8D82Fef0d77d79e5231AE7BFcFeBA2bAcF127E2B").call()/10**18

        mydict["concentrator_cvxeth_rewards"] = convex_examiner.regx_getvalue(myarray, w3, "cvxeth_rewards", "0xb1Fb0BA0676A1fFA83882c7F4805408bA232C1fA", wallet_address="0x3Cf54F3A1969be9916DAD548f3C084331C4450b5")
        mydict["concentrator_cvxeth_extracvx"] = convex_examiner.earned_grabber(myarray, w3,"cvxeth_extracvx ","0x834B9147Fd23bF131644aBC6e557Daf99C5cDa15", wallet_address="0x3Cf54F3A1969be9916DAD548f3C084331C4450b5")

        acrv = load_contract("0x2b95A1Dcc3D405535f9ed33c219ab38E8d7e0884",w3,"0x160D6e417bE17E21712F004B87872a30799Cb78f")
        mydict["acrv_totalsupply"] = acrv.totalSupply().call()/10**18
        mydict["acrv_totalunderlying"] = acrv.totalUnderlying().call()/10**18


#Keep one hour worth of data in hourly log
        myarray.append(mydict)
        while len(myarray) > 61:
            del myarray[0]
#update information on screen and pi hats when possible
        dollar_amount, mainpercentdisplay,crv_daily,cvx_daily = status_line_printer.print_status_line(carray, myarray, myarrayh, 0 - len(myarray), w3, args.Hourslookback)
        if args.Outputtohats:
            try:
                curve_hats_update(mainpercentdisplay, carray["booststatus"], mydict["ETH"])
            except Exception:
                pass
#Output dictionary to minute file
        if not args.Readonly:
            shutil.copyfile(file_name, file_name+".bak")
            json.dump(myarray, open(file_name, "w"), indent=4)
            pyportal_update(mydict, mainpercentdisplay, dollar_amount,crv_daily,cvx_daily)
#Output dictionary to hour file on the top of each hour
        if minut == "00" and mydict["claim"] > 1:
            myarrayh.append(mydict)
            if not args.Readonly:
                shutil.copyfile(file_nameh, file_nameh+".bak")
                json.dump(myarrayh, open(file_nameh, "w"), indent=4)

if __name__ == "__main__":
    main()
