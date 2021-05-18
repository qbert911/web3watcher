#!/usr/bin/env python3
"""curve"""
# pylint: disable=C0103,C0116,C0301,W0105,E0401,R0914
import sys
import json
from colorama import Fore, Style, init
init()

file_nameh = "ghistoryh.json"
usym = Fore.YELLOW + Style.BRIGHT + "$" + Style.RESET_ALL
csym = Fore.MAGENTA + Style.BRIGHT + "Ç" + Style.RESET_ALL + Fore.CYAN
with open(file_nameh, 'r') as openfile:
    myarrayh = json.load(openfile)

def byhundo(increment):
    #targetdict = [1000, 1500, 1700, 1900, 2100, 2400, 3600]
    #valuesdict = [1.11, 1.37, 1.59, 1.58, 2.06, 2.95, 2.97]
    amount = count = lastx = targetpos = 0
    print("History log starts at", myarrayh[0]["human_time"], "with a balance of", round(myarrayh[0]["claim"]))
    targetdict, valuesdict = load_sales()
    print("Using an increment of"+Style.BRIGHT+Fore.YELLOW , increment, Style.RESET_ALL+"after", targetdict[-1])
    for x in range(0, len(myarrayh)):
        if myarrayh[x]["claim"] >= targetdict[targetpos] or x == len(myarrayh) - 1:
            print("With", myarrayh[x]["invested"], "invested", end=' ')
            print("reached", csym+str(min(round(myarrayh[x]["claim"]), targetdict[targetpos]))+Style.RESET_ALL, end=' ')
            print("on", myarrayh[x]["human_time"], end='   ')
            print("[",str(round((myarrayh[x]["raw_time"] - myarrayh[lastx]["raw_time"]) / (60*60))).rjust(4), "hours ]", end='   ')
            print("avg", usym+colormodfunc(amount/count)+str(format(round(amount/count, 2), '.2f'))+Style.RESET_ALL, end='')
            if len(targetdict) - 1 == targetpos:
                targetdict.append(targetdict[targetpos] + increment)
            if len(valuesdict) > targetpos:
                print("  sold for ", valuesdict[targetpos])
            else:
                print("*")
            lastx = x
            targetpos += 1
            amount = count = 0
        else:
            amount += myarrayh[x]["USD"]
            count += 1

def load_sales():
    targetdict = []
    valuesdict = []
    runningtotal = 0
    runningamount = 0
    with open("sales.json", 'r') as thisfile:
        thisarray = json.load(thisfile)

    for x in range(0,int(len(thisarray))):
        runningtotal += thisarray[x]["amount"]
        runningamount += thisarray[x]["amount"] * thisarray[x]["value"]
        targetdict.append(runningtotal)
        valuesdict.append(thisarray[x]["value"])

    print("Sales log reports", csym+str(runningtotal)+Style.RESET_ALL, end=' ')
    print("sold for", usym+Style.BRIGHT+Fore.GREEN+str(int(runningamount))+Style.RESET_ALL, end=' ')
    print("making the overall average", Style.BRIGHT+str(round(runningamount/runningtotal,4))+Style.RESET_ALL)
    return targetdict, valuesdict

def colormodfunc(value):
    colormod = Style.BRIGHT + Fore.GREEN
    if 1 <= value < 2:
        colormod =  Fore.CYAN
    elif 2 <= value < 3:
        colormod = Fore.YELLOW
    elif value >= 3:
        colormod = Fore.RED
    return colormod

if __name__ == "__main__":
    byhundo(100)
    print("  -----  ")
    try:
        byhundo(int(sys.argv[1]))
    except:
        byhundo(1000)
