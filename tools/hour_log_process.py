#!/usr/bin/env python3
"""curve"""
# pylint: disable=C0103,C0116,C0301,W0105,E0401,R0914
import time
import json
from pycoingecko import CoinGeckoAPI
from colorama import Fore, Style, init
init()
cg = CoinGeckoAPI()

file_nameh = "history/history_archive.json"
usym = Fore.YELLOW + Style.BRIGHT + "$" + Fore.GREEN
csym = Fore.MAGENTA + Style.BRIGHT + "Ç" + Style.RESET_ALL + Fore.CYAN

def update_price(coin_type):
    USD = -1
    while USD == -1:
        try:
            USD = cg.get_price(ids=coin_type, vs_currencies='usd')[coin_type]["usd"]
        except Exception:
            time.sleep(2)
            print("Z", end='', flush=True)
    return USD

def show_me(inputs, inpute, update, isprice, invested, newline, myarrayh):
    USD = float(isprice)
    if myarrayh == 0:
        try:
            with open(file_nameh, 'r') as openfile:
                myarrayh = json.load(openfile)
        except Exception:
            print("Error reading from",file_nameh)
            return False
    try:
        totalinvested = myarrayh[inputs]["invested"]
    except Exception:
        totalinvested = 6100

    if invested == 1:
        invested = totalinvested

    while update and USD == 1:
        try:
            USD = float(update_price("curve-dao-token"))
        except Exception:
            print("PRICE BREAK")
            time.sleep(1)

    a = invested/totalinvested * USD * (myarrayh[inputs]["claim"] - myarrayh[inpute]["claim"]) #PROFIT
    b = (myarrayh[inputs]["raw_time"] - myarrayh[inpute]["raw_time"]) / (60*60) #hours elapsed
    c = round(a/b * 24*365 / invested * 100, 2)  #APR

    print("\rAt $" + Fore.YELLOW + str(format(USD, '.3f')) + Style.RESET_ALL + " per CRV = ", end='')
    print(Fore.GREEN + Style.BRIGHT + str(format(c, '.2f')) + Style.RESET_ALL + "/" + Fore.CYAN + str(format(c/USD, '.2f')) + Style.RESET_ALL + "% APR", end=' - ')
    print(usym + str(format(round(365*24*a/b, 4), '.0f')).rjust(5)  + Style.RESET_ALL + "/" + csym + str(format(365*24*a/b/USD, '.0f')).rjust(5) + Style.RESET_ALL + " per year", end=' - ')
    print(usym + str(format(round(24*a/b, 4), '.2f')).rjust(5) + Style.RESET_ALL + "/" + csym + str(format(24*a/b/USD, '.2f')).rjust(5) + Style.RESET_ALL + " per day", end=' - ')
    print(usym + str(format(round(a/b, 4), '.4f')) + Style.RESET_ALL + " / " + csym + str(format(a/b/USD, '.4f')) + Style.RESET_ALL + " per hour", end=' - ')
    if not update:  #print subtotals
        #print(usym + str(format(round(a, 2), '.2f')).rjust(5) + Style.RESET_ALL + "/" + csym + str(format(a/USD, '.2f')).rjust(5) + Style.RESET_ALL, "profit in", str(round(b)).rjust(3), "hours", end=' - ')
        print(str(round(b/24, 1)).rjust(4), "days", end=' - ')
    print("between", myarrayh[inpute]["human_time"], "and", myarrayh[inputs]["human_time"], end=' ')
    if invested != totalinvested:
        print(invested,"/", totalinvested)
    else:
        print(totalinvested, end='')
    if newline:
        print(" ")
    mytuple = a, b, c, USD, myarrayh[inpute]["human_time"], myarrayh[inputs]["human_time"]
    return mytuple

def daily_log(isprice, myportion, printit):
    b = 0
    with open(file_nameh, 'r') as openfile:
        myarrayh = json.load(openfile)
    offset = len(myarrayh)-1-(int((len(myarrayh)-1)/24)*24)
    for x in range(0, int((len(myarrayh)-1)/24)):
        thisprice = isprice
        try:
            thisprice =  myarrayh[(x*24)+24+offset]["USD"]
            if b == 0 and myarrayh[(x*24)+24+offset]["invested"] == myarrayh[-1]["invested"]:
                #if printit:
                    #print (x,myarrayh[(x*24)+24+offset]["invested"])
                b = x + 1
        except Exception:
            pass
        if printit:
            show_me((x*24)+24+offset, (x*24)+offset, 0, thisprice, myportion, 1, myarrayh)
    return b
if __name__ == "__main__":
    z=daily_log(update_price("curve-dao-token"),1,1)

    print("")
    show_me(-1, 0, 0, update_price("curve-dao-token"), 1, 1, 0)
    print("")
    show_me(-1, (z*24), 0, update_price("curve-dao-token"), 1, 1, 0)
    show_me(-1, (z*24), 0, update_price("curve-dao-token"), 1000, 1, 0)
