#!/usr/bin/env python3
"""curve"""
# pylint: disable=C0103,C0116,C0301,W0105,E0401,R0914
import time
import json
import microdotphat
from curve_rainbowhat_functions import rainbow_show_float, rainbow_show_boost_status
from colorama import Fore, Style, init
init()
from pycoingecko import CoinGeckoAPI
cg = CoinGeckoAPI()

file_nameh = "ghistoryh.json"
usym = Fore.YELLOW + Style.BRIGHT + "$" + Fore.GREEN
csym = Fore.MAGENTA + Style.BRIGHT + "Ç" + Style.RESET_ALL + Fore.CYAN

def show_me(inputs, inpute, update, isprice, invested, newline, myarrayh):
    USD = float(isprice)
    if myarrayh == 0:
        myarrayh = json.load(open(file_nameh, 'r'))
    try:
        totalinvested = myarrayh[inputs]["invested"]
    except:
        totalinvested = 6100

    if invested == 1:
        invested = totalinvested

    while update and USD == 1:
        try:
            USD = float(update_price())
        except:
            print("PRICE BREAK")
            time.sleep(1)

    a = invested/totalinvested * USD * (myarrayh[inputs]["claim"] - myarrayh[inpute]["claim"]) #PROFIT
    b = (myarrayh[inputs]["raw_time"] - myarrayh[inpute]["raw_time"]) / (60*60) #hours elapsed
    c = round(a/b * 24*365 / invested * 100, 2)  #APR

    print("\rAt $" + Fore.YELLOW + str(format(USD, '.3f')) + Style.RESET_ALL + " per CRV = ", end='')
    print(Fore.GREEN + Style.BRIGHT + str(format(c, '.2f')) + Style.RESET_ALL + "/" + Fore.CYAN + str(format(c/USD, '.2f')) + Style.RESET_ALL + "% APR", end=' - ')
    print(usym + str(format(round(365*24*a/b, 4), '.2f')).rjust(7)  + Style.RESET_ALL + "/" + csym + str(format(365*24*a/b/USD, '.2f')).rjust(7) + Style.RESET_ALL + " per year", end=' - ')
    print(usym + str(format(round(24*a/b, 4), '.2f')).rjust(4) + Style.RESET_ALL + "/" + csym + str(format(24*a/b/USD, '.2f')).rjust(4) + Style.RESET_ALL + " per day", end=' - ')
    print(usym + str(format(round(a/b, 4), '.4f')) + Style.RESET_ALL + "/" + csym + str(format(a/b/USD, '.4f')) + Style.RESET_ALL + " per hour", end=' - ')
    if not update:  #print subtotals
        #print(usym + str(format(round(a, 2), '.2f')).rjust(5) + Style.RESET_ALL + "/" + csym + str(format(a/USD, '.2f')).rjust(5) + Style.RESET_ALL, "profit in", str(round(b)).rjust(3), "hours", end=' - ')
        print(str(round(b/24, 1)), "days", end=' - ')
    print("between", myarrayh[inpute]["human_time"], "and", myarrayh[inputs]["human_time"], end='')
    if newline:
        print(" ", invested,"/", totalinvested)

def update_price():
    USD = 1
    while USD == 1:
        try:
            USD = cg.get_price(ids='curve-dao-token', vs_currencies='usd')["curve-dao-token"]["usd"]
        except:
            time.sleep(2)

    return USD

def curve_hats_update(myfloat, mystring, bootstatusarray):
    """output to rainbow and microdot hats"""
    rainbow_show_float(myfloat)
    rainbow_show_boost_status(bootstatusarray)
    microdotphat.set_clear_on_exit(False)
    microdotphat.set_rotate180(1)
    microdotphat.write_string(mystring, offset_x=0, kerning=False)
    microdotphat.show()

def daily_log(isprice, myportion):
    z = 0
    with open(file_nameh, 'r') as openfile:
        myarrayh = json.load(openfile)
    offset = len(myarrayh)-1-(int((len(myarrayh)-1)/24)*24)
    for x in range(0, int((len(myarrayh)-1)/24)):
        thisprice = isprice
        try:
            thisprice =  myarrayh[(x*24)+24+offset]["USD"]
            if z == 0 and myarrayh[(x*24)+24+offset]["invested"] == myarrayh[-1]["invested"]:
                print (x,myarrayh[(x*24)+24+offset]["invested"])
                z = x
        except:
            pass

        show_me((x*24)+24+offset, (x*24)+offset, 0, thisprice, myportion, 1, myarrayh)
    return z
if __name__ == "__main__":
    z=daily_log(update_price(),2000)

    print("")
    show_me(-1, 0, 0, update_price(), 1, 1, 0)
    #show_me(-1, -(8*24), 0, update_price(), 1, 1, 0)
    show_me(-1, (z*24), 0, update_price(), 1, 1, 0)
    show_me(-1, (z*24), 0, update_price(), 3200, 1, 0)
    print("    ")
