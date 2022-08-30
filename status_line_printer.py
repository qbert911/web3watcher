#!/usr/bin/env python3
"""curve"""
# pylint: disable=C0103,C0301,W0105,E0401,R0914,C0411,W0702,C0200,C0116,w0106
import time
from colorama import Fore, Style
from tools.ens_helper import ipfs_hash_value

curve_ipfs_current_hash="Qmap8m62DnovFjN7jpdvbqhiBuQsipux2gEKLFjQmiNrqB"

def show_convex(myarray, eoa, extramins, name, label, extrapools, token_value,showdetails):
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
    
    subtotal=round(tprofit/((myarray[eoa][name][0]+.000000001)*pricefactor[1])*100, 2)
    if showdetails:
        print(Fore.RED+Style.BRIGHT+label+Style.RESET_ALL+str(format(subtotal, '5.2f')).rjust(5), end=' ')
        print(Style.DIM+"\b{"+buffer+"}"+Style.RESET_ALL, end=' ')
    else:
        print(str(format(subtotal, '2.0f')).rjust(2)+"%", end=' ')

def show_cvx_virt(myarray,  myarrayh,lookback,name):
    _, _, _, minut = map(str, time.strftime("%m %d %H %M").split())
    try:
        tprofit=(myarray[-1][name]-myarrayh[-lookback-1][name])*24*365/(lookback+float(int(minut)/60))
        #thisdiff = (myarray[-1][carray["name"][i]+"profit"]-myarrayh[-lookback-1][carray["name"][i]+"profit"])/(lookback+float(int(minut)/60))
        subtotal=str(format(round(tprofit*100, 4), '5.2f')).rjust(5)
    except Exception:
        subtotal="xx.xx"

    print(Fore.GREEN+Style.DIM+subtotal+Style.RESET_ALL, end=' ')

def show_convex2(myarray, eoa, extramins, name, label, extrapools, token_value,myarrayh,lookback,name2,showdetails):
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
        tvirt = 0
        subvirt="xx.xx"
    subtotal=round( ((tprofit/((myarray[eoa][name][0]+.000000001)*pricefactor[extrapools])) +tvirt)*100, 2)

    if showdetails:
        print(Fore.RED+Style.BRIGHT+label+Style.RESET_ALL+str(format(subtotal, '5.2f')).rjust(5)[0:5], end=' ')
        print(Style.DIM+"\b{"+Fore.GREEN+subvirt+Fore.WHITE+buffer+"}"+Style.RESET_ALL, end=' ')
    else:
        print(str(format(subtotal, '2.0f')).rjust(2)+"%", end=' ')

def show_convex2_extrafxs(myarray, eoa, extramins, name, label, extrapools, token_value,myarrayh,lookback,name2,showdetails):
    """cvx display"""
    _, _, _, minut = map(str, time.strftime("%m %d %H %M").split())
    labels = [ "I", "v", "x", "t"]
    pricefactor = [ token_value, myarray[-1]["USD"], myarray[-1]["USDcvx"], myarray[-1]["USD3pool"]]
    buffer=""
    tprofit=0
    #extrafxs
    thisdiff=(myarray[-1]["fxslocked_extrafxs"]-myarray[eoa]["fxslocked_extrafxs"])/(60+extramins)*myarray[-1]["FRAX"]*60*24*365
    buffer+=Fore.RED+"f"+Fore.WHITE
    if thisdiff >= 0:
        tprofit+=thisdiff
        buffer+=str(format(round((myarray[-1]["fxslocked_extrafxs"]-myarray[eoa]["fxslocked_extrafxs"])/(60+extramins)*myarray[-1]["FRAX"]*60*24*365/(myarray[eoa][name][0]*pricefactor[extrapools])*100, 2), '.2f')).rjust(5)+""
    else:
        buffer+="xx.xx"
    #crv and cvx main 
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
    #extracvx
    thisdiff=(myarray[-1]["fxslocked_extracvx"]-myarray[eoa]["fxslocked_extracvx"])/(60+extramins)*myarray[-1]["USDcvx"]*60*24*365
    buffer+=Fore.RED+"X"+Fore.WHITE
    if thisdiff >= 0:
        tprofit+=thisdiff
        buffer+=str(format(round((myarray[-1]["fxslocked_extracvx"]-myarray[eoa]["fxslocked_extracvx"])/(60+extramins)*myarray[-1]["USDcvx"]*60*24*365/(myarray[eoa][name][0]*pricefactor[extrapools])*100, 2), '.2f')).rjust(5)+""
    else:
        buffer+="xx.xx" 
    
    try:
        tvirt=(myarray[-1][name2]-myarrayh[-lookback-1][name2])*24*365/(lookback+float(int(minut)/60))
        subvirt=str(format(round(tvirt*100, 4), '5.2f')).rjust(5)
    except Exception:
        subvirt="xx.xx"
    subtotal=round( ((tprofit/((myarray[eoa][name][0]+.000000001)*pricefactor[extrapools])) +tvirt)*100, 2)

    if showdetails:
        print(Fore.RED+Style.BRIGHT+label+Style.RESET_ALL+str(format(subtotal, '5.2f')).rjust(5), end=' ')
        print(Style.DIM+"\b{"+Fore.GREEN+subvirt+Fore.WHITE+buffer+"}"+Style.RESET_ALL, end=' ')
    else:
        print(str(format(subtotal, '2.0f')).rjust(2)+"%", end=' ')

def show_convex2_extracvx(myarray, eoa, extramins, name, label, extrapools, token_value,myarrayh,lookback,name2,showdetails,extracvxname):
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
    #extracvx
    thisdiff=(myarray[-1][extracvxname]-myarray[eoa][extracvxname])/(60+extramins)*myarray[-1]["USDcvx"]*60*24*365
    buffer+=Fore.RED+"X"+Fore.WHITE
    if thisdiff >= 0:
        tprofit+=thisdiff
        buffer+=str(format(round((myarray[-1][extracvxname]-myarray[eoa][extracvxname])/(60+extramins)*myarray[-1]["USDcvx"]*60*24*365/(myarray[eoa][name][0]*pricefactor[extrapools])*100, 2), '.2f')).rjust(5)+""
    else:
        buffer+="xx.xx" 
    try:
        tvirt=(myarray[-1][name2]-myarrayh[-lookback-1][name2])*24*365/(lookback+float(int(minut)/60))
        subvirt=str(format(round(tvirt*100, 4), '5.2f')).rjust(5)
    except Exception:
        subvirt="xx.xx"
    subtotal=round( ((tprofit/((myarray[eoa][name][0]+.000000001)*pricefactor[extrapools])) +tvirt)*100, 2)

    if showdetails:
        print(Fore.RED+Style.BRIGHT+label+Style.RESET_ALL+str(format(subtotal, '5.2f')).rjust(5), end=' ')
        print(Style.DIM+"\b{"+Fore.GREEN+subvirt+Fore.WHITE+buffer+"}"+Style.RESET_ALL, end =' ')
    else:
        print(str(format(subtotal, '2.0f')).rjust(2)+"%", end=' ')

def show_cvxlocked_rewards(myarray, eoa, extramins,showdetails):
    """cvx locking rewards display"""
    try:
        tprofit=max(0,float(myarray[-1]["cvxlocked_rewards"][1])-float(myarray[eoa]["cvxlocked_rewards"][1]))/(60+extramins)*myarray[-1]["USDcvxCRV"]*60*24*365
        subtotal=round(tprofit/(myarray[eoa]["cvxlocked_rewards"][0]*myarray[-1]["USDcvx"])*100, 2)
    except Exception:
        subtotal="xx.xx"

    if showdetails:
        print(Fore.RED+Style.BRIGHT+"xCVX"+Style.RESET_ALL+str(format(subtotal, '5.2f')).rjust(5), end=' ')
    else:
        print(str(format(subtotal, '2.0f')).rjust(2)+"%", end=' ')

def show_curve(carray, myarray, myarrayh, eoa, extramins, lookback, showdetails):
    tprofit = 0
    buffer = ""
    tripool_token_price =  3 * ((myarray[-1]["BTC"] * myarray[-1]["ETH"])**(1/3))
    tripool_value_modifyer_in = tripool_token_price / 1229
    _, _, _, minut = map(str, time.strftime("%m %d %H %M").split())
    for i in range(0, len(carray["name"])):
        if carray["currentboost"][i] > 0:
            buffer+=Fore.RED+Style.BRIGHT+carray["name"][i]+Style.RESET_ALL
            tripool_value_modifyer = 1
            if carray["name"][i] == "R":
                tripool_value_modifyer = tripool_value_modifyer_in
            try:
                subtotal = round((myarray[-1][carray["name"][i]+"pool"]-myarray[eoa][carray["name"][i]+"pool"])/(60+extramins)*60*myarray[-1]["USD"]*24*365/(carray["invested"][i]*tripool_value_modifyer)*100, 2)
                buffer+=str(format(subtotal, '.2f')).rjust(5)[0:5]
            except Exception:
                buffer+="xx.xx"
            try:
                thisdiff = (myarray[-1][carray["name"][i]+"profit"]-myarrayh[-lookback-1][carray["name"][i]+"profit"])/(lookback+float(int(minut)/60))
            except Exception:
                thisdiff = -1

            if thisdiff >= 0:
                tprofit += thisdiff
                buffer += Style.DIM+Fore.GREEN+str(format(round(thisdiff/60*60*myarray[-1]["USD"]*24*365/(carray["invested"][i]*tripool_value_modifyer)*100, 2), '.2f')).rjust(5)[0:5]+" "+Style.RESET_ALL
            else:
                buffer += Style.DIM+Fore.GREEN+"xx.xx "+Style.RESET_ALL
    if showdetails:
        print(buffer, end='')
    else:
        print(str(format(subtotal, '2.0f')).rjust(2)+"%", end=' ')
        
        
def show_difference(myarray,eoa):

    extramins = round((myarray[-1]["raw_time"]-myarray[eoa]["raw_time"])/60)+eoa+1
    curveclaim_hourly = max(0,(myarray[-1]["claim"]-myarray[eoa]["claim"])) / (60+extramins)*60
    spelleth_hourly = max(0,myarray[-1]["spelleth_rewards"][1]-myarray[eoa]["spelleth_rewards"][1]\
                +((myarray[-1]["spelleth_rewards"][2]-myarray[eoa]["spelleth_rewards"][2])*myarray[-1]["USDcvx"]/myarray[-1]["USD"]))\
                / (60+extramins)*60

    crvstaked_hourly = max(0,myarray[-1]["crvstaked_rewards"][1]-myarray[eoa]["crvstaked_rewards"][1]\
                +((myarray[-1]["crvstaked_rewards"][2]-myarray[eoa]["crvstaked_rewards"][2])*myarray[-1]["USDcvx"]/myarray[-1]["USD"])\
                +((myarray[-1]["crvstaked_rewards"][3]-myarray[eoa]["crvstaked_rewards"][3])/myarray[-1]["USD"]))\
                / (60+extramins)*60  
    
    cvxlocked_hourly = max(0,((myarray[-1]["cvxlocked_rewards"][1]-myarray[eoa]["cvxlocked_rewards"][1])*myarray[-1]["USDcvxCRV"]/myarray[-1]["USD"]))\
                / (60+extramins)*60

    cvxeth_hourly = max(0,myarray[-1]["cvxeth_rewards"][1]-myarray[eoa]["cvxeth_rewards"][1]\
                +((myarray[-1]["cvxeth_rewards"][2]-myarray[eoa]["cvxeth_rewards"][2])*myarray[-1]["USDcvx"]/myarray[-1]["USD"])\
                +((myarray[-1]["cvxeth_extracvx"]-myarray[eoa]["cvxeth_extracvx"])*myarray[-1]["USDcvx"]/myarray[-1]["USD"]))\
                / (60+extramins)*60   

    fxslocked_hourly = max(0,myarray[-1]["fxslocked_rewards"][1]-myarray[eoa]["fxslocked_rewards"][1]\
                +((myarray[-1]["fxslocked_rewards"][2]-myarray[eoa]["fxslocked_rewards"][2])*myarray[-1]["USDcvx"]/myarray[-1]["USD"])\
                +((myarray[-1]["fxslocked_extracvx"]-myarray[eoa]["fxslocked_extracvx"])*myarray[-1]["USDcvx"]/myarray[-1]["USD"])\
                +((myarray[-1]["fxslocked_extrafxs"]-myarray[eoa]["fxslocked_extrafxs"])*myarray[-1]["FRAX"]/myarray[-1]["USD"]))\
                / (60+extramins)*60

    crvsquared_hourly = max(0,myarray[-1]["crvsquared_rewards"][1]-myarray[eoa]["crvsquared_rewards"][1]\
                +((myarray[-1]["crvsquared_rewards"][2]-myarray[eoa]["crvsquared_rewards"][2])*myarray[-1]["USDcvx"]/myarray[-1]["USD"])\
                +((myarray[-1]["crvsquared_extracvx"]-myarray[eoa]["crvsquared_extracvx"])*myarray[-1]["USDcvx"]/myarray[-1]["USD"]))\
                / (60+extramins)*60

    diffcrv = max(0,(myarray[-1]["claim"]-myarray[eoa]["claim"])) +\
              max(0,((myarray[-1]["cvxlocked_rewards"][1]-myarray[eoa]["cvxlocked_rewards"][1])*myarray[-1]["USDcvxCRV"]/myarray[-1]["USD"])) +\
              max(0,myarray[-1]["crvsquared_rewards"][1]-myarray[eoa]["crvsquared_rewards"][1]) +\
              max(0,myarray[-1]["cvxeth_rewards"][1]-myarray[eoa]["cvxeth_rewards"][1]) +\
              max(0,myarray[-1]["spelleth_rewards"][1]-myarray[eoa]["spelleth_rewards"][1]) +\
              max(0,myarray[-1]["fxslocked_rewards"][1]-myarray[eoa]["fxslocked_rewards"][1]) +\
              max(0,myarray[-1]["crvstaked_rewards"][1]-myarray[eoa]["crvstaked_rewards"][1])

    diffcvx = max(0,myarray[-1]["cvxeth_rewards"][2]-myarray[eoa]["cvxeth_rewards"][2]) +\
              max(0,myarray[-1]["cvxeth_extracvx"]-myarray[eoa]["cvxeth_extracvx"])+\
              max(0,myarray[-1]["crvsquared_rewards"][2]-myarray[eoa]["crvsquared_rewards"][2]) +\
              max(0,myarray[-1]["crvsquared_extracvx"]-myarray[eoa]["crvsquared_extracvx"])+\
              max(0,myarray[-1]["spelleth_rewards"][2]-myarray[eoa]["spelleth_rewards"][2]) +\
              max(0,myarray[-1]["fxslocked_rewards"][2]-myarray[eoa]["fxslocked_rewards"][2]) +\
              max(0,myarray[-1]["crvstaked_rewards"][2]-myarray[eoa]["crvstaked_rewards"][2])+\
              max(0,myarray[-1]["fxslocked_extracvx"]-myarray[eoa]["fxslocked_extracvx"])+\
              max(0,(myarray[-1]["fxslocked_extrafxs"]-myarray[eoa]["fxslocked_extrafxs"])*myarray[-1]["FRAX"]/myarray[-1]["USDcvx"])

    diff3pool = max(0,myarray[-1]["crvstaked_rewards"][3]-myarray[eoa]["crvstaked_rewards"][3])  

    acrv_coefficient = myarray[-1]["acrv_totalunderlying"]/myarray[-1]["acrv_totalsupply"]
    my_pool_percent = (1/acrv_coefficient)* 211 / myarray[-1]["concentrator_cvxeth_rewards"][0] #HACK
    ctr_unclaimed_current =  (my_pool_percent *(myarray[-1]["concentrator_cvxeth_rewards"][1]\
                +(myarray[-1]["concentrator_cvxeth_rewards"][2]*myarray[-1]["USDcvx"]/myarray[-1]["USD"])\
                +(myarray[-1]["concentrator_cvxeth_extracvx"]*myarray[-1]["USDcvx"]/myarray[-1]["USD"])))
    
    ctr_unclaimed_past = ((1/acrv_coefficient)*211 / myarray[eoa]["concentrator_cvxeth_rewards"][0] *(myarray[eoa]["concentrator_cvxeth_rewards"][1]\
                +(myarray[eoa]["concentrator_cvxeth_rewards"][2]*myarray[-1]["USDcvx"]/myarray[-1]["USD"])\
                +(myarray[eoa]["concentrator_cvxeth_extracvx"]*myarray[-1]["USDcvx"]/myarray[-1]["USD"])))
    concentrator_hourly = (ctr_unclaimed_current-ctr_unclaimed_past\
                +myarray[-1]['concentrator_rewards_CTR']-myarray[eoa]['concentrator_rewards_CTR'])*acrv_coefficient\
                / (60+extramins)*60

    print("D$"+format((round((curveclaim_hourly + spelleth_hourly)*24*myarray[-1]['USD'], 0)), '.0f').rjust(2)+"/",end="")
    print(format((round(fxslocked_hourly*24*myarray[-1]['USD'], 0)), '.0f').rjust(2)+"/"+Style.RESET_ALL,end="")
    print(format((round(cvxeth_hourly*24*myarray[-1]['USD'], 2)), '.1f').rjust(3)+"/"+Style.RESET_ALL,end="")
    print(format((round(concentrator_hourly*24*myarray[-1]['USD'], 2)), '.0f').rjust(3)+"/"+Style.RESET_ALL,end="") #HACK
    print(format((round(crvsquared_hourly*24*myarray[-1]['USD'], 0)), '.0f').rjust(2)+"/"+Style.RESET_ALL,end="")
    print(format((round((crvstaked_hourly + cvxlocked_hourly)*24*myarray[-1]['USD'], 0)), '.0f').rjust(2)+Style.RESET_ALL,end="")

    dbuffer=Fore.RED+"t"+Fore.WHITE+format((round(diff3pool*24/(60+extramins)*60, 2)), '.0f').rjust(2)
    dbuffer+=Fore.RED+"v"+Fore.WHITE+format((round(diffcrv*24/(60+extramins)*60, 2)), '.0f').rjust(2)
    dbuffer+=Fore.RED+"r"+Fore.WHITE+format((round(concentrator_hourly*24, 2)), '.0f').rjust(2)
    dbuffer+=Fore.RED+"x"+Fore.WHITE+format((round(diffcvx*24/(60+extramins)*60, 2)), '.2f').rjust(4)

    print(Style.DIM+"{"+dbuffer+"}"+Style.RESET_ALL,end="")
    
    cvxeth_token_price = 2 * myarray[-1]["cvxeth_virt"] * ((myarray[-1]["USDcvx"] * myarray[-1]["ETH"])**(1/2))
    spelleth_token_price = 2 * myarray[-1]["spelleth_virt"] * ((myarray[-1]["SPELL"] * myarray[-1]["ETH"])**(1/2))
    fxslocked_token_price = 2 * myarray[-1]["fxslocked_virt"] * ((myarray[-1]["FRAX"] * (myarray[-1]["FRAX"]*myarray[-1]["fxslocked_oracle"]))**(1/2)) #hack

    concentrator_yearly = concentrator_hourly*24*myarray[-1]['USD'] *365

    print(f"{myarray[-1]['concentrator_rewards_CTR']:4.1f}",end='')
    print(f"+{ctr_unclaimed_current:5.2f}",end=" ") #-{ctr_unclaimed_past:5.2f}
    #print(f"{myarray[-1]['concentrator_totalmined']/1000:.0f}|${dollar_value_total_ctr_earned:.0f}",end=" ")
    print(Fore.RED+Style.BRIGHT+"IFO"+Style.RESET_ALL+Fore.WHITE+f"{concentrator_yearly/(211*cvxeth_token_price)*100:5.2f}",end=" ")

    totalvalue = ((myarray[-1]["cvxeth_rewards"][0]+211)*cvxeth_token_price)+\
                  (myarray[-1]["spelleth_rewards"][0]*spelleth_token_price)+\
                  (myarray[-1]["fxslocked_rewards"][0]*fxslocked_token_price)+\
                  (myarray[-1]["crvstaked_rewards"][0]*myarray[-1]['USD'])+\
                  (myarray[-1]["crvsquared_rewards"][0]*myarray[-1]['USD'])+\
                  (myarray[-1]["cvxlocked_rewards"][0]*myarray[-1]['USDcvx'])
    #curveclaim_hourly + 
    daily_dollar_amount = (concentrator_hourly+(spelleth_hourly)+(crvstaked_hourly + cvxlocked_hourly)+cvxeth_hourly+crvsquared_hourly+fxslocked_hourly)*24*myarray[-1]['USD']
    mainpercentdisplay = daily_dollar_amount *365/totalvalue *100

    return daily_dollar_amount, mainpercentdisplay,diffcrv*24/(60+extramins)*60,diffcvx*24/(60+extramins)*60

def print_status_line(carray, myarray, myarrayh, eoa, w3, lookback):
    """print main status line"""
    extramins = round((myarray[-1]["raw_time"]-myarray[eoa]["raw_time"])/60)+eoa+1
    #crveth_token_price = 2 * myarray[-1]["crveth_virt"] * ((myarray[-1]["USD"] * myarray[-1]["ETH"])**(1/2))
    cvxeth_token_price = 2 * myarray[-1]["cvxeth_virt"] * ((myarray[-1]["USDcvx"] * myarray[-1]["ETH"])**(1/2))
    spelleth_token_price = 2 * myarray[-1]["spelleth_virt"] * ((myarray[-1]["SPELL"] * myarray[-1]["ETH"])**(1/2))
    fxslocked_token_price = 2 * myarray[-1]["fxslocked_virt"] * ((myarray[-1]["FRAX"] * (myarray[-1]["FRAX"]*myarray[-1]["fxslocked_oracle"]))**(1/2)) #hack
    tripool_token_price =  3 * ((myarray[-1]["BTC"] * myarray[-1]["ETH"])**(1/3))
    tripool_value_modifyer = tripool_token_price / 1229

    #Start line with time and price information
    print("\r",end='',flush=True)
    print(myarray[-1]["human_time"], end=' - ')

    #show daily differnce calculations   
    daily_dollar_amount, mainpercentdisplay,crv_hourly,cvx_hourly = show_difference(myarray,eoa)

    #show vestiges of raw tri-pool (non-convex) ecosystem
    #curve_functions.curve_boost_check(carray, w3)
    #print("["+Fore.BLUE+f"{100*round(tripool_value_modifyer-1,2):2.0f}"+Style.RESET_ALL+"%]", end=' ')
    show_curve(carray, myarray, myarrayh, eoa, extramins, lookback, True)
 
    #show profitability percentages for each convex contract
    #show_convex2(myarray, eoa,extramins,"spelleth_rewards","xS2E", 0, spelleth_token_price,myarrayh,lookback,"spelleth_virt",True) #Indicates no third pool and using token_value_modifyer
    show_convex2_extrafxs(myarray, eoa,extramins,"fxslocked_rewards","xFXS", 0, fxslocked_token_price,myarrayh,lookback,"fxslocked_virt",True)
    #show_convex2(myarray, eoa,extramins,"crveth_rewards","xV2E", 0, crveth_token_price, myarrayh,lookback,"crveth_virt",True) #Indicates no third pool and using token_value_modifyer
    show_convex2_extracvx(myarray, eoa,extramins,"cvxeth_rewards","xX2E", 0, cvxeth_token_price, myarrayh,lookback,"cvxeth_virt",True,"cvxeth_extracvx") #Indicates no third pool and using token_value_modifyer
    show_convex2_extracvx(myarray, eoa,extramins,"crvsquared_rewards","xV2V", 0, myarray[-1]['USDcvxCRV'], myarrayh,lookback,"crvsquared_virt",True,"crvsquared_extracvx") #Indicates no third pool and using token_value_modifyer
    show_convex(myarray, eoa,extramins,"crvstaked_rewards","xCRV", 1, 1,True) #Indicates having an extra 3pool and not using token_value_modifyer
    show_cvxlocked_rewards(myarray, eoa, extramins,True)
    
    #show crv / cvxcrv price differential
    print("["+Fore.CYAN+Style.BRIGHT+f"{((myarray[-1]['USDcvxCRV']-myarray[-1]['USD'])/myarray[-1]['USD'])*100:5.2f}"+Style.RESET_ALL+"%]",end="")
    
    #air bubble extra minutes
    if extramins > 0:
        print(Fore.RED+str(extramins)+Style.RESET_ALL, end=' ')

    #fewer than 60 records in the ghistory.json file
    if eoa > -61:
        print(Fore.RED+Style.BRIGHT+str(61+eoa).rjust(2)+Style.RESET_ALL, end=' ')

    #check to see if amounts have changed
    if myarray[-1]["invested"] != myarray[eoa]["invested"]:
        print(Fore.RED+str(round(myarray[-1]["invested"] - myarray[eoa]["invested"]))+Style.RESET_ALL, end=' ')
    if myarray[-1]["crvstaked_rewards"][0] != myarray[eoa]["crvstaked_rewards"][0]:
        print(Fore.RED+str(round(myarray[-1]["crvstaked_rewards"][0] - myarray[eoa]["crvstaked_rewards"][0]))+Style.RESET_ALL, end='v ')
    if myarray[-1]["cvxlocked_rewards"][0] != myarray[eoa]["cvxlocked_rewards"][0]:
        print(Fore.RED+str(round(myarray[-1]["cvxlocked_rewards"][0] - myarray[eoa]["cvxlocked_rewards"][0]))+Style.RESET_ALL, end='x ')
    if myarray[-1]["fxslocked_rewards"][0] != myarray[eoa]["fxslocked_rewards"][0]:
        print(Fore.RED+str(round(myarray[-1]["fxslocked_rewards"][0] - myarray[eoa]["fxslocked_rewards"][0]))+Style.RESET_ALL, end='f ')
    #try:  #check to see if the interface linked on ipfs has changed
    #    if ipfs_hash_value(w3, 'curve.eth', True) != curve_ipfs_current_hash:
    #        print(Fore.RED+Style.BRIGHT+"WW"+Style.RESET_ALL, end=' ')
    #    else:
    #        print("W", end=' ')
    #except:
    #    print(Fore.WHITE+Style.DIM+"w"+Style.RESET_ALL, end=' ')

    return daily_dollar_amount, mainpercentdisplay,crv_hourly,cvx_hourly #to pass to pyportal

if __name__ == "__main__":
    print("this module is not meant to be run solo")
