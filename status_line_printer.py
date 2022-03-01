#!/usr/bin/env python3
"""curve"""
# pylint: disable=C0103,C0301,W0105,E0401,R0914,C0411,W0702,C0200,C0116,w0106
import time
from colorama import Fore, Style
import curve_functions
from tools.ens_helper import ipfs_hash_value

curve_ipfs_current_hash="Qmap8m62DnovFjN7jpdvbqhiBuQsipux2gEKLFjQmiNrqB"

def show_convex(myarray, eoa, extramins, name, label, extrapools, token_value):
    """cvx display"""
    labels = [ "t", "v", "x"]
    pricefactor = [ myarray[-1]["USD3pool"], myarray[-1]["USD"], myarray[-1]["USDcvx"]]
    buffer=""
    tprofit=0
    for i in range(0,3):
        buffer+=Fore.RED+labels[i]+Fore.WHITE
        try:
            l = i
            if i == 0:
                l = 3
            thisdiff=(myarray[-1][name][l]-myarray[eoa][name][l])/(60+extramins)*pricefactor[i]*60*24*365
            if thisdiff >= 0:
                tprofit+=thisdiff
                buffer+=str(format(round(thisdiff/(myarray[eoa][name][0]*pricefactor[1])*100, 2), '.2f')).rjust(5)+""
            else:
                buffer+="xx.xx"
        except Exception:
            buffer+="xx.xx"
        subtotal=str(format(round(tprofit/((myarray[eoa][name][0]+.000000001)*pricefactor[1])*100, 2), '5.2f')).rjust(5)

    print(Fore.RED+Style.BRIGHT+label+Style.RESET_ALL+subtotal+Style.DIM+"{"+buffer+"}"+Style.RESET_ALL, end=' ')

def show_cvx_virt(myarray,  myarrayh,lookback,name):
    _, _, _, minut = map(str, time.strftime("%m %d %H %M").split())
    try:
        tprofit=(myarray[-1][name]-myarrayh[-lookback-1][name])*24*365/(lookback+float(int(minut)/60))
        #thisdiff = (myarray[-1][carray["name"][i]+"profit"]-myarrayh[-lookback-1][carray["name"][i]+"profit"])/(lookback+float(int(minut)/60))
        subtotal=str(format(round(tprofit*100, 4), '5.2f')).rjust(5)
    except Exception:
        subtotal="xx.xx"

    print(Fore.GREEN+Style.DIM+subtotal+Style.RESET_ALL, end=' ')

def show_convex2(myarray, eoa, extramins, name, label, extrapools, token_value,myarrayh,lookback,name2):
    """cvx display"""
    _, _, _, minut = map(str, time.strftime("%m %d %H %M").split())
    labels = [ "I", "v", "x", "t"]
    pricefactor = [ token_value, myarray[-1]["USD"], myarray[-1]["USDcvx"], myarray[-1]["USD3pool"]]
    buffer=""
    tprofit=0
    for i in range(1,3+extrapools):
        buffer+=Fore.RED+labels[i]+Fore.WHITE
        try:
            thisdiff=(myarray[-1][name][i]-myarray[eoa][name][i])/(60+extramins)*pricefactor[i]*60*24*365
            if thisdiff >= 0:
                tprofit+=thisdiff
                buffer+=str(format(round((myarray[-1][name][i]-myarray[eoa][name][i])/(60+extramins)*pricefactor[i]*60*24*365/(myarray[eoa][name][0]*pricefactor[extrapools])*100, 2), '.2f')).rjust(5)+""
            else:
                buffer+="xx.xx"
        except Exception:
            buffer+="xx.xx"
    try:
        tvirt=(myarray[-1][name2]-myarrayh[-lookback-1][name2])*24*365/(lookback+float(int(minut)/60))
        subvirt=str(format(round(tvirt*100, 4), '5.2f')).rjust(5)
    except Exception:
        subvirt="xx.xx"
    subtotal=str(format(round( ((tprofit/((myarray[eoa][name][0]+.000000001)*pricefactor[extrapools])) +tvirt)*100, 2), '5.2f')).rjust(5)

    print(Fore.RED+Style.BRIGHT+label+Style.RESET_ALL+subtotal+Style.DIM+"{"+Fore.GREEN+subvirt+Fore.WHITE+buffer+"}"+Style.RESET_ALL, end=' ')

def show_cvx_rewards(myarray, eoa, extramins):
    """cvx staking rewards display"""
    try:
        tprofit=(myarray[-1]["cvxcrv_rewards"][1]-myarray[eoa]["cvxcrv_rewards"][1])/(60+extramins)*myarray[-1]["USDcvxCRV"]*60*24*365
        subtotal=str(format(round(tprofit/(myarray[eoa]["cvxcrv_rewards"][0]*myarray[-1]["USDcvx"])*100, 2), '5.2f')).rjust(5)
    except Exception:
        subtotal="xx.xx"

    print(Fore.RED+Style.BRIGHT+"xCVX"+Style.RESET_ALL+subtotal, end=' ')

def show_curve(carray, myarray, myarrayh, eoa, extramins, USD, lookback, tripool_value_modifyer_in):
    tprofit = 0
    buffer = ""
    _, _, _, minut = map(str, time.strftime("%m %d %H %M").split())
    for i in range(0, len(carray["name"])):
        if carray["currentboost"][i] > 0:
            buffer+=Fore.RED+Style.BRIGHT+carray["name"][i]+Style.RESET_ALL
            tripool_value_modifyer = 1
            if carray["name"][i] == "R":
                tripool_value_modifyer = tripool_value_modifyer_in
            try:
                buffer+=str(format(round((myarray[-1][carray["name"][i]+"pool"]-myarray[eoa][carray["name"][i]+"pool"])/(60+extramins)*60*USD*24*365/(carray["invested"][i]*tripool_value_modifyer)*100, 2), '.2f')).rjust(5)[0:5]
            except Exception:
                buffer+="xx.xx"
            try:
                thisdiff = (myarray[-1][carray["name"][i]+"profit"]-myarrayh[-lookback-1][carray["name"][i]+"profit"])/(lookback+float(int(minut)/60))
            except Exception:
                thisdiff = -1

            if thisdiff >= 0:
                tprofit += thisdiff
                buffer += Style.DIM+Fore.GREEN+str(format(round(thisdiff/60*60*USD*24*365/(carray["invested"][i]*tripool_value_modifyer)*100, 2), '.2f')).rjust(5)[0:5]+" "+Style.RESET_ALL
            else:
                buffer += Style.DIM+Fore.GREEN+"xx.xx "+Style.RESET_ALL
    print(buffer, end='')

def show_difference(myarray,eoa):

    extramins = round((myarray[-1]["raw_time"]-myarray[eoa]["raw_time"])/60)+eoa
    diffa = max(0,(myarray[-1]["claim"]-myarray[eoa]["claim"]))
    diffb = max(0,myarray[-1]["trix_rewards"][1]-myarray[eoa]["trix_rewards"][1]\
                +((myarray[-1]["trix_rewards"][2]-myarray[eoa]["trix_rewards"][2])*myarray[-1]["USDcvx"]/myarray[-1]["USD"]))
    difff = max(0,myarray[-1]["mimx_rewards"][1]-myarray[eoa]["mimx_rewards"][1]\
                +((myarray[-1]["mimx_rewards"][2]-myarray[eoa]["mimx_rewards"][2])*myarray[-1]["USDcvx"]/myarray[-1]["USD"]))
    diffh = max(0,myarray[-1]["spelleth_rewards"][1]-myarray[eoa]["spelleth_rewards"][1]\
                +((myarray[-1]["spelleth_rewards"][2]-myarray[eoa]["spelleth_rewards"][2])*myarray[-1]["USDcvx"]/myarray[-1]["USD"]))

    difference = (diffa + diffb + difff + diffh) / (60+extramins)*60

    diffc = max(0,myarray[-1]["cvx_rewards"][1]-myarray[eoa]["cvx_rewards"][1]\
                +((myarray[-1]["cvx_rewards"][2]-myarray[eoa]["cvx_rewards"][2])*myarray[-1]["USDcvx"]/myarray[-1]["USD"]))
    diffd = max(0,((myarray[-1]["cvxcrv_rewards"][1]-myarray[eoa]["cvxcrv_rewards"][1])*myarray[-1]["USDcvxCRV"]/myarray[-1]["USD"]))

    diffe = max(0,myarray[-1]["cvxeth_rewards"][1]-myarray[eoa]["cvxeth_rewards"][1]\
                +((myarray[-1]["cvxeth_rewards"][2]-myarray[eoa]["cvxeth_rewards"][2])*myarray[-1]["USDcvx"]/myarray[-1]["USD"]))

    diffg = max(0,myarray[-1]["crveth_rewards"][1]-myarray[eoa]["crveth_rewards"][1]\
                +((myarray[-1]["crveth_rewards"][2]-myarray[eoa]["crveth_rewards"][2])*myarray[-1]["USDcvx"]/myarray[-1]["USD"]))


    difference_afterparty = (diffc + diffd) / (60+extramins)*60
    difference_afterparty2 = (diffe) / (60+extramins)*60

    difference_afterparty3 = (diffg) / (60+extramins)*60

    diffcrv = diffa + diffd + max(0,myarray[-1]["trix_rewards"][1]-myarray[eoa]["trix_rewards"][1]) +\
                              max(0,myarray[-1]["mimx_rewards"][1]-myarray[eoa]["mimx_rewards"][1]) +\
                              max(0,myarray[-1]["crveth_rewards"][1]-myarray[eoa]["crveth_rewards"][1]) +\
                              max(0,myarray[-1]["cvxeth_rewards"][1]-myarray[eoa]["cvxeth_rewards"][1]) +\
                              max(0,myarray[-1]["spelleth_rewards"][1]-myarray[eoa]["spelleth_rewards"][1]) +\
                              max(0,myarray[-1]["cvx_rewards"][1]-myarray[eoa]["cvx_rewards"][1])
    diffcvx = max(0,myarray[-1]["cvxeth_rewards"][2]-myarray[eoa]["cvxeth_rewards"][2]) +\
              max(0,myarray[-1]["trix_rewards"][2]-myarray[eoa]["trix_rewards"][2]) +\
              max(0,myarray[-1]["mimx_rewards"][2]-myarray[eoa]["mimx_rewards"][2]) +\
              max(0,myarray[-1]["crveth_rewards"][2]-myarray[eoa]["crveth_rewards"][2]) +\
              max(0,myarray[-1]["spelleth_rewards"][2]-myarray[eoa]["spelleth_rewards"][2]) +\
              max(0,myarray[-1]["cvx_rewards"][2]-myarray[eoa]["cvx_rewards"][2])

    #   print(Fore.GREEN+Style.BRIGHT+str(format(round((difference)*USD*24*365/(sum(carray["invested"])+myarray[-1]["mimx_rewards"][0]+(myarray[-1]["trix_rewards"][0]*tripool_token_price)+(myarray[-1]["spelleth_rewards"][0]*spelleth_token_price))*100, 2), '5.2f'))+Style.RESET_ALL+"/", end='')
    #   print(Fore.YELLOW+str(format(round((tprofit/60*60)*24*365/sum(carray["invested"])*100, 2), '5.2f'))[0:5]+Style.RESET_ALL+"% APR", end=' - ')

    print("D$"+format((round(difference*24*myarray[-1]['USD'], 0)), '.0f').rjust(2)+"/",end="")
    print(format((round(difference_afterparty3*24*myarray[-1]['USD'], 0)), '.0f').rjust(3)+"/"+Style.RESET_ALL,end="")
    print(format((round(difference_afterparty2*24*myarray[-1]['USD'], 0)), '.0f').rjust(3)+"/"+Style.RESET_ALL,end="")
    print(format((round(difference_afterparty*24*myarray[-1]['USD'], 0)), '.0f').rjust(2)+Style.RESET_ALL,end="")
    dbuffer=Fore.RED+"v"+Fore.WHITE+format((round(diffcrv*24/(60+extramins)*60, 2)), '.2f').rjust(5)
    dbuffer+=Fore.RED+"x"+Fore.WHITE+format((round(diffcvx*24/(60+extramins)*60, 2)), '.2f').rjust(4)
    print(Style.DIM+"{"+dbuffer+"}"+Style.RESET_ALL,end=" ")

    crveth_token_price = 2 * myarray[-1]["crveth_virt"] * ((myarray[-1]["USD"] * myarray[-1]["ETH"])**(1/2))
    cvxeth_token_price = 2 * myarray[-1]["cvxeth_virt"] * ((myarray[-1]["USDcvx"] * myarray[-1]["ETH"])**(1/2))

    myvalue = 100*(difference_afterparty2 + difference_afterparty3)*myarray[-1]['USD']*24*365 / ((myarray[-1]["cvxeth_rewards"][0]*cvxeth_token_price)+(myarray[-1]["crveth_rewards"][0]*crveth_token_price))
    dollar_amount = (difference+difference_afterparty+difference_afterparty2+difference_afterparty3)*24*myarray[-1]['USD']

    return myvalue, dollar_amount

def print_status_line(carray, myarray, myarrayh, USD, eoa, w3, lookback):
    """print main status line"""
    extramins = round((myarray[-1]["raw_time"]-myarray[eoa]["raw_time"])/60)+eoa
    crveth_token_price = 2 * myarray[-1]["crveth_virt"] * ((myarray[-1]["USD"] * myarray[-1]["ETH"])**(1/2))
    cvxeth_token_price = 2 * myarray[-1]["cvxeth_virt"] * ((myarray[-1]["USDcvx"] * myarray[-1]["ETH"])**(1/2))
    spelleth_token_price = 2 * myarray[-1]["spelleth_virt"] * ((myarray[-1]["SPELL"] * myarray[-1]["ETH"])**(1/2))
    tripool_token_price =  3 * ((myarray[-1]["BTC"] * myarray[-1]["ETH"])**(1/3))
    tripool_value_modifyer = tripool_token_price / 1229

    #Start line with time and price information
    print("\r",end='',flush=True)
    print(myarray[-1]["human_time"], end=' ')
    print("$"+Fore.YELLOW+Style.BRIGHT+f"{USD:5.2f}"+Style.RESET_ALL, end=' ') #csym+"1"+Style.RESET_ALL+" = "+
    print("$"+Fore.YELLOW+f"{myarray[-1]['USDcvx']:5.2f}"+Style.RESET_ALL,end=" ", flush=True)
    print("($"+Fore.YELLOW+Style.DIM+f"{myarray[-1]['SPELL']:6.4f}"+Style.RESET_ALL,end=" ", flush=True)
    print("$"+Fore.MAGENTA+f"{myarray[-1]['FRAX']:5.2f}"+Style.RESET_ALL,end=") - ", flush=True)

    #show daily differnce calculations   
    myvalue, dollar_amount = show_difference(myarray,eoa)

    #show vestiges of raw tri-pool (non-convex) ecosystem
    curve_functions.curve_boost_check(carray, w3)
    show_curve(carray, myarray, myarrayh, eoa, extramins, USD, lookback, tripool_value_modifyer)
    print("["+Fore.BLUE+f"{100*round(tripool_value_modifyer-1,2):2.0f}"+Style.RESET_ALL+"%]", end=' ')

    #show profitability percentages for each convex contract
    show_convex2(myarray, eoa,extramins,"spelleth_rewards","xS2E", 0, spelleth_token_price,myarrayh,lookback,"spelleth_virt") #Indicates no third pool and using token_value_modifyer
    show_convex2(myarray, eoa,extramins,"crveth_rewards","xV2E", 0, crveth_token_price, myarrayh,lookback,"crveth_virt") #Indicates no third pool and using token_value_modifyer
    show_convex2(myarray, eoa,extramins,"cvxeth_rewards","xX2E", 0, cvxeth_token_price, myarrayh,lookback,"cvxeth_virt") #Indicates no third pool and using token_value_modifyer
    show_convex(myarray, eoa,extramins,"cvx_rewards","xCRV", 1, 1) #Indicates having an extra 3pool and not using token_value_modifyer
     #show_convex(carray, myarray, eoa,extramins,"trix_rewards","xTri", 0, tripool_token_price) #Indicates no third pool and using token_value_modifyer
     #show_convex(myarray, eoa,extramins,"mimx_rewards","xMim", 0, 1) #Indicates no third pool and not using token_value_modifyer
    show_cvx_rewards(myarray, eoa, extramins)
 
    #show crv / cvxcrv price differential
    print("["+Fore.CYAN+Style.BRIGHT+f"{((myarray[-1]['USDcvxCRV']-myarray[-1]['USD'])/myarray[-1]['USD'])*100:5.2f}"+Style.RESET_ALL+"%]",end=" ")
    
    #air bubble extra minutes
    if extramins >= 0: 
        print(Fore.RED+str(round((myarray[-1]["raw_time"]-myarray[eoa]["raw_time"])/60)+eoa+1)+Style.RESET_ALL, end=' ')

    #fewer than 60 records in the ghistory.json file
    if eoa > -61:  
        print(Fore.RED+Style.BRIGHT+str(61+eoa).rjust(2)+Style.RESET_ALL, end=' ')

    #check to see if amounts have changed
    if myarray[-1]["invested"] != myarray[eoa]["invested"]:
        print(Fore.RED+str(round(myarray[-1]["invested"] - myarray[eoa]["invested"]))+Style.RESET_ALL, end=' ')
    if myarray[-1]["cvx_rewards"][0] != myarray[eoa]["cvx_rewards"][0]:
        print(Fore.RED+str(round(myarray[-1]["cvx_rewards"][0] - myarray[eoa]["cvx_rewards"][0]))+Style.RESET_ALL, end='v ')
    if myarray[-1]["trix_rewards"][0] != myarray[eoa]["trix_rewards"][0]:
        print(Fore.RED+str(round(myarray[-1]["trix_rewards"][0] - myarray[eoa]["trix_rewards"][0]))+Style.RESET_ALL, end='z ')
    if myarray[-1]["mimx_rewards"][0] != myarray[eoa]["mimx_rewards"][0]:
        print(Fore.RED+str(round(myarray[-1]["mimx_rewards"][0] - myarray[eoa]["mimx_rewards"][0]))+Style.RESET_ALL, end='t ')
    if myarray[-1]["cvxcrv_rewards"][0] != myarray[eoa]["cvxcrv_rewards"][0]:
        print(Fore.RED+str(round(myarray[-1]["cvxcrv_rewards"][0] - myarray[eoa]["cvxcrv_rewards"][0]))+Style.RESET_ALL, end='x ')
    #try:  #check to see if the interface linked on ipfs has changed
    #    if ipfs_hash_value(w3, 'curve.eth', True) != curve_ipfs_current_hash:
    #        print(Fore.RED+Style.BRIGHT+"WW"+Style.RESET_ALL, end=' ')
    #    else:
    #        print("W", end=' ')
    #except:
    #    print(Fore.WHITE+Style.DIM+"w"+Style.RESET_ALL, end=' ')

    return dollar_amount, myvalue #to pass to pyportal

if __name__ == "__main__":
    print("this module is not meant to be run solo")
