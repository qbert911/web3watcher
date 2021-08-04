#!/usr/bin/env python3
"""curve"""
# pylint: disable=C0103,C0116,C0301,W0105,E0401,R0914
import datetime
import json
from hour_log_process import show_me
from price_getter import update_price
from colorama import Fore, Style, init
init()

file_nameh = "../history/history_archive.json"
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

    print("Log starts at:",myarrayh[0]["human_time"],"with a balance of",round(myarrayh[0]["claim"],2))

    for x in range(0, int(len(myarrayh))):
        if not myarrayh[wasinvested]["invested"] == myarrayh[x]["invested"] or x==int(len(myarrayh))-1:
            newinvestment = x
            amount_generated = round(myarrayh[x]["claim"] - myarrayh[wasinvested]["claim"],2)
            totalprofit += amount_generated
            da = round((myarrayh[newinvestment]["raw_time"]-myarrayh[wasinvested]["raw_time"]) / (60*60*24),1)
            if printit:
                print(usym+str(myarrayh[newinvestment-1]["invested"])+Style.RESET_ALL, end='(')
                print(str(format((myarrayh[newinvestment-0]["invested"]-myarrayh[newinvestment-1]["invested"]),'+.0f')).rjust(5), end=') - ')
                print(myarrayh[newinvestment]["human_time"], end=' - ')
                print(str(da).rjust(4),"days" ,end=' - ')
                print(csym+str(round(amount_generated)).rjust(3)+Style.RESET_ALL, end=' - ')
                #print(format(round(amount_generated/max(da*24,.00001)/myarrayh[newinvestment]["invested"]*1000,4), '.4f'), end=' - ')

            mypercent=0
            for i in range(0,len(invarray["invested"])):
                if invarray["raw_time"][i] <= myarrayh[newinvestment]["raw_time"]:
                    mypercent += (invarray["invested"][i]/myarrayh[newinvestment-1]["invested"])
                    mypercentme = (invarray["invested"][i]/myarrayh[newinvestment-1]["invested"])
                    if printit:
                        print(invarray["person"][i][0], str(invarray["invested"][i]).rjust(4), end=' ')
                        print("("+str(format(round(mypercentme*100,2), '5.2f'))+"%)",csym+str(format(round(mypercentme*amount_generated,2),'.2f')).rjust(6)+Style.RESET_ALL, end=' - ')
                    try:
                        profitdict[invarray["person"][i]] = round(profitdict[invarray["person"][i]]+(invarray["invested"][i]/myarrayh[newinvestment-1]["invested"]*amount_generated),2)
                    except Exception:
                        profitdict[invarray["person"][i]] = round(invarray["invested"][i]/myarrayh[newinvestment-1]["invested"]*amount_generated,2)
            if printit:
                print(Fore.YELLOW+"B rest"+Style.RESET_ALL, end=' ')
                print("("+str(format(round((1-mypercent)*100,2), '5.2f'))+"%)",csym+str(format(round((1-mypercent)*amount_generated,2),'.2f')).rjust(6)+Style.RESET_ALL, end=' - ')

            mytuple = myarrayh[newinvestment-1]["invested"], myarrayh[newinvestment]["human_time"], da, amount_generated,round(mypercent,4)
            epochsdict.append(mytuple)
            if printit:
                print("\b\b ")
            wasinvested = newinvestment

    profitdict["rest"] = totalprofit+myarrayh[0]["claim"]
    for key in profitdict:
        if key != "rest":
            profitdict["rest"] = round(profitdict["rest"] - profitdict[key],2)
    profitdict["all"] = totalprofit
    return epochsdict, profitdict

if __name__ == "__main__":
    aa=show_me(-1, 0, 0, update_price("curve-dao-token"), 1, 1, 0)
    #print(aa)
    epochsdic, profitdic = find_epochs("all",1)
    print (profitdic)
    #print (epochsdic)
