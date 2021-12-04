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
import convex_examiner
import curve_functions
import status_line_printer

cursor.hide()                               #don't draw the cursor
init()                                      #initialize colorama

INFURA_ID = "9c51dd19cb9e456387014e7d1661afa3"

infura_w3 = Web3(Web3.HTTPProvider('https://mainnet.infura.io/v3/'+INFURA_ID))
#mylocal_w3 = Web3(Web3.HTTPProvider('http://192.168.0.4:8545'))
mylocal_w3 = Web3(Web3.WebsocketProvider("ws://192.168.0.4:8546"))

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

def wait_for_local_node_sync(w3):
    while True:
        try:
            a = w3.eth.syncing
            #print(a,"\r", end="")
            try:
                blockdiff = a['highestBlock']-a['currentBlock']
            except Exception:
                blockdiff = 0
            if a is False or blockdiff < 15:
                break
            print("\rLocal Node has:",blockdiff, "blocks left to catch up\r", end="")
        except Exception:
            print("\rLocal Node communication error", end="")
        time.sleep(10)

def key_capture_thread():
    global enter_hit
    enter_hit = False
    input()
    enter_hit = True

def pyportal_update(display_percent, booststatusarray, tripool_value_modifyer):
    pyportal_dict = {}
    pyportal_dict["display_percent"] = display_percent
    #pyportal_dict["booststatus"] = booststatusarray
    pyportal_dict["tripool_value_modifyer"] = round(tripool_value_modifyer, 5)
    try:
        json.dump(pyportal_dict, open("pyportal_tmp.json", "w"), indent=4)
        shutil.copyfile("pyportal_tmp.json", "pyportal.json")
    except:
        print("error writing to pyportal.json")

def show_headers(w3):
    virutal_price_sum=curve_functions.curve_header_display(myarray, carray, w3, args.Fullheader)
    convex_examiner.convex_header_display(myarray, carray, w3)
    curve_functions.combined_stats_display(myarray, carray, w3, virutal_price_sum)
    threading.Thread(target=key_capture_thread, args=(), name='key_capture_thread', daemon=True).start()

def gas_and_sleep(w3, mydict):
    firstpass = True                                                            #Prevent header display from outputting in conflict with regular update
    mydict["USD"] = update_price("curve-dao-token",'▸','▹')
    mydict["USDcvx"] = update_price("convex-finance",'▸','▹')
    mydict["USDcvxCRV"] = update_price("convex-crv",'▸','▹')
    mydict["USD3pool"] = 1.02 #update_price("lp-3pool-curve")
    mydict["ETH"] = update_price("ethereum",'▸','▹')
    #mydict["SUSHI"] = update_price("sushi",'▸','▹')
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
        wait_for_local_node_sync(w3)
    print("\r",end="")

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
        print("Local Node Found:", w3.isConnected())
        wait_for_local_node_sync(w3)
    curve_functions.load_curvepools_fromjson(myarray, carray, w3)
    show_headers(w3)
#Main program loop starts here
    while True:
#Check gas price every 10 seconds and wait for a minute to pass
        mydict = {}
        gas_and_sleep(w3, mydict)
#Update dictionary values and price information
        month, day, hour, minut = map(str, time.strftime("%m %d %H %M").split())
        mydict["raw_time"] = round(time.time())
        mydict["human_time"] = month+"/"+day+" "+hour+":"+minut
        mydict["invested"] = sum(carray["invested"])
        mydict["cvxcrv_rewards"] = convex_examiner.cvxcrv_getvalue(False, myarray, w3)
        mydict["trix_rewards"] = convex_examiner.regx_getvalue(False, myarray, w3, "trix_rewards", "0x9D5C5E364D81DaB193b72db9E9BE9D8ee669B652")
        mydict["mimx_rewards"] = convex_examiner.regx_getvalue(False, myarray, w3, "mimx_rewards", "0xC62DE533ea77D46f3172516aB6b1000dAf577E89")
        mydict["crveth_rewards"] = convex_examiner.regx_getvalue(False, myarray, w3, "crveth_rewards", "0x085A2054c51eA5c91dbF7f90d65e728c0f2A270f",1)
        mydict["cvx_rewards"] = convex_examiner.cvx_getvalue(False, myarray, w3)
        mydict["cvxsushi_rewards"] = convex_examiner.cvxsushi_getvalue(False, myarray, w3)
        curve_functions.update_curve_pools(mydict, carray, myarray, myarrayh, w3)
#Keep one hour worth of data in hourly log
        myarray.append(mydict)
        if len(myarray) > 61:
            del myarray[0]
#update information on screen and pi hats when possible
        display_percent, tripool_value_modifyer = status_line_printer.print_status_line(carray, myarray, myarrayh, myarray[-1]["USD"], 0 - len(myarray), w3, args.Hourslookback)
        if args.Outputtohats:
            try:
                curve_hats_update(display_percent, carray["booststatus"], mydict["ETH"])
            except Exception:
                pass
#Output dictionary to minute file
        if not args.Readonly:
            shutil.copyfile(file_name, file_name+".bak")
            json.dump(myarray, open(file_name, "w"), indent=4)
            pyportal_update(display_percent, carray["booststatus"], tripool_value_modifyer)
#Output dictionary to hour file on the top of each hour
        if minut == "00" and mydict["claim"] > 1:
            myarrayh.append(mydict)
            if not args.Readonly:
                shutil.copyfile(file_nameh, file_nameh+".bak")
                json.dump(myarrayh, open(file_nameh, "w"), indent=4)

if __name__ == "__main__":
    main()
