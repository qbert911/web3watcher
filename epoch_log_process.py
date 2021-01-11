#!/usr/bin/env python3
"""curve"""
# pylint: disable=C0103,C0116,C0301,W0105,E0401,R0914
import datetime
import time
import json
from curve_log_process import show_me, update_price
from colorama import Fore, Style, init
init()


file_nameh = "ghistoryh.json"
usym = Fore.YELLOW + Style.BRIGHT + "$" + Fore.GREEN
csym = Fore.MAGENTA + Style.BRIGHT + "Ç" + Style.RESET_ALL + Fore.CYAN

def show_me2(inputs, inpute, update, isprice, invested, newline, myarrayh):
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

def load_investor_epochs(targetperson):
    datarray = { "invested": [], "person" : [], "humantime": [], "raw_time":[] }
    with open("investments.json", 'r') as thisfile:
        thisarray = json.load(thisfile)

    for x in range(0,int(len(thisarray))):
        if thisarray[x]["person"] == targetperson:
            humantime = thisarray[x]['date_in']
            y, m, d = int(humantime[0:4]), int(humantime[5:7]), int(humantime[8:10])
            datarray["raw_time"].append(round(datetime.datetime(y, m, d, 0, 0).timestamp()))
            datarray["invested"].append(thisarray[x]["invested"])
            datarray["person"].append(thisarray[x]["person"])
            datarray["humantime"].append(thisarray[x]["date_in"])

    return datarray
def find_epochs():
    invarray = load_investor_epochs("maureen")
    print(invarray,invarray["invested"])
    profitdict = {}
    epochsdict = []
    wasinvested = 0
    with open(file_nameh, 'r') as openfile:
        myarrayh = json.load(openfile)

    print("Log starts at:",myarrayh[0]["human_time"],"with a balance of",round(myarrayh[0]["claim"]))

    for x in range(0, int(len(myarrayh))):
        if not myarrayh[wasinvested]["invested"] == myarrayh[x]["invested"] or x==int(len(myarrayh))-1:
            newinvestment = x
            amount_generated = round(myarrayh[x]["claim"] - myarrayh[wasinvested]["claim"],2)
            da = round((myarrayh[newinvestment]["raw_time"]-myarrayh[wasinvested]["raw_time"]) / (60*60*24),1)
            ya = amount_generated/max(da*24,.00001)
            print(myarrayh[newinvestment-1]["invested"], end=' - ')
            #print(myarrayh[newinvestment]["raw_time"], end=' - ')
            print(myarrayh[newinvestment]["human_time"], end=' - ')
            print(da,"days" ,end=' - ')
            print(round(myarrayh[newinvestment]["claim"]), end=' - ')
            print(amount_generated, end=' - ')
            print(round(ya/myarrayh[newinvestment]["invested"]*1000,4), end=' - ')

            mypercent=0
            for i in range(0,len(invarray["invested"])):
                if invarray["raw_time"][i] <= myarrayh[newinvestment]["raw_time"]:
                    print (invarray["person"][i], invarray["invested"][i], myarrayh[newinvestment-1]["invested"], amount_generated, end=' - ')
                    mypercent += (invarray["invested"][i]/myarrayh[newinvestment-1]["invested"])
                    print(round(mypercent,4),round(mypercent*amount_generated,2), end=' - ')
                    try:
                        profitdict[invarray["person"][i]] = round(profitdict[invarray["person"][i]]+(invarray["invested"][i]/myarrayh[newinvestment-1]["invested"]*amount_generated),2)
                    except:
                        profitdict[invarray["person"][i]] = round(invarray["invested"][i]/myarrayh[newinvestment-1]["invested"]*amount_generated,2)

            mytuple = myarrayh[newinvestment-1]["invested"], myarrayh[newinvestment]["human_time"], da, amount_generated, ya,round(mypercent,4)
            epochsdict.append(mytuple)


            print("\b\b ")
            wasinvested=newinvestment

    return epochsdict, profitdict

if __name__ == "__main__":
    show_me2(-1, 0, 0, update_price(), 1, 1, 0)
    #darray = { "invested": [], "person" : [], "humantime": [], "raw_time":[] }
    #load_investor_epochs(darray)
    #print(darray)
    epochsdict, profitdict = find_epochs()
    print (profitdict)
    print (epochsdict)
    #print(darray)
#    show_me2(-1, -(z*2), 0, curve_log_process.update_price(), 1, 1, 0)
#    show_me2(-1, -(z*2), 0, curve_log_process.update_price(), 2000, 1, 0)
    print("    ")
