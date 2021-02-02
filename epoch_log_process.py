#!/usr/bin/env python3
"""curve"""
# pylint: disable=C0103,C0116,C0301,W0105,E0401,R0914
import datetime
import time
import json
from curve_log_process import show_me, update_price, show_me
from colorama import Fore, Style, init
init()

file_nameh = "ghistoryh.json"
usym = Fore.YELLOW + Style.BRIGHT + "$" + Fore.GREEN
csym = Fore.MAGENTA + Style.BRIGHT + "Ç" + Style.RESET_ALL + Fore.CYAN

def load_investor_epochs(targetperson):
    datarray = { "invested": [], "person" : [], "humantime": [], "raw_time":[] }
    with open("investments.json", 'r') as thisfile:
        thisarray = json.load(thisfile)

    for x in range(0,int(len(thisarray))):
        if thisarray[x]["person"] == targetperson or targetperson=="all":
            humantime = thisarray[x]['date_in']
            y, m, d = int(humantime[0:4]), int(humantime[5:7]), int(humantime[8:10])
            datarray["raw_time"].append(round(datetime.datetime(y, m, d, 0, 0).timestamp()))
            datarray["invested"].append(thisarray[x]["invested"])
            datarray["person"].append(thisarray[x]["person"])
            datarray["humantime"].append(thisarray[x]["date_in"])

    return datarray

def find_epochs(targetperson,printit):
    invarray = load_investor_epochs(targetperson)
    #print(invarray, invarray["invested"])
    profitdict = {}
    epochsdict = []
    wasinvested = 0
    totalprofit = 0
    with open(file_nameh, 'r') as openfile:
        myarrayh = json.load(openfile)

    #print("Log starts at:",myarrayh[0]["human_time"],"with a balance of",round(myarrayh[0]["claim"]))

    for x in range(0, int(len(myarrayh))):
        if not myarrayh[wasinvested]["invested"] == myarrayh[x]["invested"] or x==int(len(myarrayh))-1:
            newinvestment = x
            amount_generated = round(myarrayh[x]["claim"] - myarrayh[wasinvested]["claim"],2)
            totalprofit += amount_generated
            da = round((myarrayh[newinvestment]["raw_time"]-myarrayh[wasinvested]["raw_time"]) / (60*60*24),1)
            if printit:
                print(myarrayh[newinvestment-1]["invested"], end=' - ')
                print(myarrayh[newinvestment-0]["invested"]-myarrayh[newinvestment-1]["invested"], end=' - ')
                print(myarrayh[newinvestment]["human_time"], end=' - ')
                print(da,"days" ,end=' - ')
                print(round(myarrayh[newinvestment]["claim"]), end=' - ')
                print(amount_generated, end=' - ')
                print(round(amount_generated/max(da*24,.00001)/myarrayh[newinvestment]["invested"]*1000,4), end=' - ')

            mypercent=0
            for i in range(0,len(invarray["invested"])):
                if invarray["raw_time"][i] <= myarrayh[newinvestment]["raw_time"]:
                    mypercent += (invarray["invested"][i]/myarrayh[newinvestment-1]["invested"])
                    if printit:
                        print (invarray["person"][i], invarray["invested"][i], myarrayh[newinvestment-1]["invested"], amount_generated, end=' - ')
                        print(round(mypercent,4),round(mypercent*amount_generated,2), end=' - ')
                    try:
                        profitdict[invarray["person"][i]] = round(profitdict[invarray["person"][i]]+(invarray["invested"][i]/myarrayh[newinvestment-1]["invested"]*amount_generated),2)
                    except:
                        profitdict[invarray["person"][i]] = round(invarray["invested"][i]/myarrayh[newinvestment-1]["invested"]*amount_generated,2)

            mytuple = myarrayh[newinvestment-1]["invested"], myarrayh[newinvestment]["human_time"], da, amount_generated,round(mypercent,4)
            epochsdict.append(mytuple)
            if printit:
                print("\b\b ")
            wasinvested=newinvestment
    profitdict["all"]=totalprofit
    return epochsdict, profitdict

if __name__ == "__main__":
    aa=show_me(-1, 0, 0, update_price(), 1, 1, 0)
    print(aa)
    epochsdic, profitdic = find_epochs("all",1)
    print (profitdic)
    print (epochsdic)
