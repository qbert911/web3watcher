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
    for i in range(3):
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
        tvirt=(myarray[-1][name][4]-myarrayh[-lookback-1][name][4])*24*365/(lookback+float(int(minut)/60))
        subvirt=str(format(round(tvirt*100, 4), '5.2f')).rjust(5)
    except Exception:
        subvirt="xx.xx"
    subtotal=round( ((tprofit/((myarray[eoa][name][0]+.000000001)*pricefactor[extrapools])) +tvirt)*100, 2)

    if showdetails:
        print(Fore.RED+Style.BRIGHT+label+Style.RESET_ALL+str(format(subtotal, '5.2f')).rjust(5)[:5], end=' ')
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
    thisdiff=(myarray[-1]["fxslocked_rewards"][3][1]['amount']-myarray[eoa]["fxslocked_rewards"][3][1]['amount'])/(60+extramins)*myarray[-1]["FRAX"]*60*24*365
    buffer+=Fore.RED+"f"+Fore.WHITE
    if thisdiff >= 0:
        tprofit+=thisdiff
        buffer+=str(format(round((myarray[-1]["fxslocked_rewards"][3][1]['amount']-myarray[eoa]["fxslocked_rewards"][3][1]['amount'])/(60+extramins)*myarray[-1]["FRAX"]*60*24*365/(myarray[eoa][name][0]*pricefactor[extrapools])*100, 2), '.2f')).rjust(5)+""
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
    thisdiff=(myarray[-1]["fxslocked_rewards"][3][0]['amount']-myarray[eoa]["fxslocked_rewards"][3][0]['amount'])/(60+extramins)*myarray[-1]["USDcvx"]*60*24*365
    buffer+=Fore.RED+"X"+Fore.WHITE
    if thisdiff >= 0:
        tprofit+=thisdiff
        buffer+=str(format(round((myarray[-1]["fxslocked_rewards"][3][0]['amount']-myarray[eoa]["fxslocked_rewards"][3][0]['amount'])/(60+extramins)*myarray[-1]["USDcvx"]*60*24*365/(myarray[eoa][name][0]*pricefactor[extrapools])*100, 2), '.2f')).rjust(5)+""
    else:
        buffer+="xx.xx" 
    
    try:
        tvirt=(myarray[-1][name][4]-myarrayh[-lookback-1][name][4])*24*365/(lookback+float(int(minut)/60))
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
    thisdiff=(myarray[-1][name][3][0]['amount']-myarray[eoa][name][3][0]['amount'])/(60+extramins)*myarray[-1]["USDcvx"]*60*24*365
    buffer+=Fore.RED+"X"+Fore.WHITE
    if thisdiff >= 0:
        tprofit+=thisdiff
        buffer+=str(format(round((myarray[-1][name][3][0]['amount']-myarray[eoa][name][3][0]['amount'])/(60+extramins)*myarray[-1]["USDcvx"]*60*24*365/(max(myarray[eoa][name][0],.0000001)*pricefactor[extrapools])*100, 2), '.2f')).rjust(5)+""
    else:
        buffer+="xx.xx" 
    try:
        tvirt=(myarray[-1][name][4]-myarrayh[-lookback-1][name][4])*24*365/(lookback+float(int(minut)/60))
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
    for i in range(len(carray["name"])):
        if carray["currentboost"][i] > 0:
            buffer+=Fore.RED+Style.BRIGHT+carray["name"][i]+Style.RESET_ALL
            tripool_value_modifyer = 1
            if carray["name"][i] == "R":
                tripool_value_modifyer = tripool_value_modifyer_in
            try:
                subtotal = round((myarray[-1][carray["name"][i]+"pool"]-myarray[eoa][carray["name"][i]+"pool"])/(60+extramins)*60*myarray[-1]["USD"]*24*365/(carray["invested"][i]*tripool_value_modifyer)*100, 2)
                buffer+=str(format(subtotal, '.2f')).rjust(5)[:5]
            except Exception:
                buffer+="xx.xx"
            try:
                thisdiff = (myarray[-1][carray["name"][i]+"profit"]-myarrayh[-lookback-1][carray["name"][i]+"profit"])/(lookback+float(int(minut)/60))
            except Exception:
                thisdiff = -1

            if thisdiff >= 0:
                tprofit += thisdiff
                buffer += Style.DIM+Fore.GREEN+str(format(round(thisdiff/60*60*myarray[-1]["USD"]*24*365/(carray["invested"][i]*tripool_value_modifyer)*100, 2), '.2f')).rjust(5)[:5]+" "+Style.RESET_ALL
            else:
                buffer += Style.DIM+Fore.GREEN+"xx.xx "+Style.RESET_ALL
    if showdetails:
        print(buffer, end='')
    else:
        print(str(format(subtotal, '2.0f')).rjust(2)+"%", end=' ')

def show_abra(myarray, eoa, extramins,showdetails):
    try:
        tprofit=max(0,float(myarray[-1]["abra_spelleth"][2])-float(myarray[eoa]["abra_spelleth"][2]))/(60+extramins)*myarray[-1]["SPELL"]*60*24*365
        subtotal=round(tprofit/((myarray[-1]["abra_spelleth"][0]*myarray[-1]["ETH"])+(myarray[-1]["abra_spelleth"][1]*myarray[-1]["SPELL"]))*100, 2)
    except Exception:
        subtotal="xx.xx"

    if showdetails:
        print(Fore.RED+Style.BRIGHT+"aS2E"+Style.RESET_ALL+str(format(subtotal, '5.2f')).rjust(5), end=' ')
    else:
        print(str(format(subtotal, '2.0f')).rjust(2)+"%", end=' ')

def calc_concentrator_hourly(myarray,eoa,extramins,myarrayh,lookback):
    CONCENTRATOR_FEE = .95
    ctr_unclaimed_local_max = local_max = local_max_value = 0
    if myarray[-1]['concentrator_cvxeth_rewards'][1] < myarray[eoa]['concentrator_cvxeth_rewards'][1]:   #harvester function was called in the past hour
        for z in range(-1,eoa-1,-1):
            if myarray[z]["concentrator_cvxeth_rewards"][1] > local_max_value:
                local_max = z
                local_max_value = myarray[z]["concentrator_cvxeth_rewards"][1]
        ctr_unclaimed_local_max = CONCENTRATOR_FEE * (211 * myarray[local_max]["concentrator_x2e_virt"] / myarray[local_max]["concentrator_cvxeth_rewards"][0] *(myarray[local_max]["concentrator_cvxeth_rewards"][1]\
                +(myarray[local_max]["concentrator_cvxeth_rewards"][2]*myarray[local_max]["USDcvx"]/myarray[local_max]["USD"])\
                +(myarray[local_max]["concentrator_cvxeth_rewards"][3][0]['amount']*myarray[local_max]["USDcvx"]/myarray[local_max]["USD"])))
        #print(local_max,round(ctr_unclaimed_local_max,2),end='') 

    ctr_unclaimed_current_crv = CONCENTRATOR_FEE * (211* myarray[-1]["concentrator_x2e_virt"]  / myarray[-1]["concentrator_cvxeth_rewards"][0] *(myarray[-1]["concentrator_cvxeth_rewards"][1]\
                +(myarray[-1]["concentrator_cvxeth_rewards"][2]*myarray[-1]["USDcvx"]/myarray[-1]["USD"])\
                +(myarray[-1]["concentrator_cvxeth_rewards"][3][0]['amount']*myarray[-1]["USDcvx"]/myarray[-1]["USD"])))
    
    ctr_unclaimed_past_crv = CONCENTRATOR_FEE * (211 * myarray[eoa]["concentrator_x2e_virt"] / myarray[eoa]["concentrator_cvxeth_rewards"][0] *(myarray[eoa]["concentrator_cvxeth_rewards"][1]\
                +(myarray[eoa]["concentrator_cvxeth_rewards"][2]*myarray[-1]["USDcvx"]/myarray[-1]["USD"])\
                +(myarray[eoa]["concentrator_cvxeth_rewards"][3][0]['amount']*myarray[-1]["USDcvx"]/myarray[-1]["USD"])))
    ctr_unclaimed_tvirt = (myarray[-1]["concentrator_cvxeth_rewards"][4] - myarrayh[-lookback-1]["concentrator_cvxeth_rewards"][4])*24*365/lookback
    #tvirt=(myarray[-1][name][4]-myarrayh[-lookback-1][name][4])*24*365/(lookback+float(int(minut)/60))
    concentrator_hourly_crv = max(0,(ctr_unclaimed_current_crv-ctr_unclaimed_past_crv+ctr_unclaimed_local_max)\
                #+((myarray[-1]['concentrator_rewards_CTR']-myarray[eoa]['concentrator_rewards_CTR'])*myarray[-1]["concentrator_virt"]))\
                / (60+extramins)*60)
    diffctr = concentrator_hourly_crv/myarray[-1]["concentrator_virt"]*myarray[-1]["USDcvxCRV"]/myarray[-1]["USD"]            
    ctr_unclaimed_current = ctr_unclaimed_current_crv/myarray[-1]["concentrator_virt"] #*myarray[-1]["USDcvxCRV"]/myarray[-1]["USD"]
    return concentrator_hourly_crv, ctr_unclaimed_current, diffctr,ctr_unclaimed_tvirt

def show_difference(myarray,eoa,myarrayh,lookback):

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
                +((myarray[-1]["cvxeth_rewards"][3][0]['amount']-myarray[eoa]["cvxeth_rewards"][3][0]['amount'])*myarray[-1]["USDcvx"]/myarray[-1]["USD"]))\
                / (60+extramins)*60   

    fxslocked_hourly = max(0,myarray[-1]["fxslocked_rewards"][1]-myarray[eoa]["fxslocked_rewards"][1]\
                +((myarray[-1]["fxslocked_rewards"][2]-myarray[eoa]["fxslocked_rewards"][2])*myarray[-1]["USDcvx"]/myarray[-1]["USD"])\
                +((myarray[-1]["fxslocked_rewards"][3][0]['amount']-myarray[eoa]["fxslocked_rewards"][3][0]['amount'])*myarray[-1]["USDcvx"]/myarray[-1]["USD"])\
                +((myarray[-1]["fxslocked_rewards"][3][1]['amount']-myarray[eoa]["fxslocked_rewards"][3][1]['amount'])*myarray[-1]["FRAX"]/myarray[-1]["USD"]))\
                / (60+extramins)*60

    crvsquared_hourly = max(0,myarray[-1]["crvsquared_rewards"][1]-myarray[eoa]["crvsquared_rewards"][1]\
                +((myarray[-1]["crvsquared_rewards"][2]-myarray[eoa]["crvsquared_rewards"][2])*myarray[-1]["USDcvx"]/myarray[-1]["USD"])\
                +((myarray[-1]["crvsquared_rewards"][3][0]['amount']-myarray[eoa]["crvsquared_rewards"][3][0]['amount'])*myarray[-1]["USDcvx"]/myarray[-1]["USD"]))\
                / (60+extramins)*60

    diffcrv = max(0,(myarray[-1]["claim"]-myarray[eoa]["claim"])) +\
              max(0,((myarray[-1]["cvxlocked_rewards"][1]-myarray[eoa]["cvxlocked_rewards"][1])*myarray[-1]["USDcvxCRV"]/myarray[-1]["USD"])) +\
              max(0,myarray[-1]["crvsquared_rewards"][1]-myarray[eoa]["crvsquared_rewards"][1]) +\
              max(0,myarray[-1]["cvxeth_rewards"][1]-myarray[eoa]["cvxeth_rewards"][1]) +\
              max(0,myarray[-1]["spelleth_rewards"][1]-myarray[eoa]["spelleth_rewards"][1]) +\
              max(0,myarray[-1]["fxslocked_rewards"][1]-myarray[eoa]["fxslocked_rewards"][1]) +\
              max(0,myarray[-1]["crvstaked_rewards"][1]-myarray[eoa]["crvstaked_rewards"][1])

    diffcvx = max(0,myarray[-1]["cvxeth_rewards"][2]-myarray[eoa]["cvxeth_rewards"][2]) +\
              max(0,myarray[-1]["cvxeth_rewards"][3][0]['amount']-myarray[eoa]["cvxeth_rewards"][3][0]['amount'])+\
              max(0,myarray[-1]["crvsquared_rewards"][2]-myarray[eoa]["crvsquared_rewards"][2]) +\
              max(0,myarray[-1]["crvsquared_rewards"][3][0]['amount']-myarray[eoa]["crvsquared_rewards"][3][0]['amount'])+\
              max(0,myarray[-1]["spelleth_rewards"][2]-myarray[eoa]["spelleth_rewards"][2]) +\
              max(0,myarray[-1]["fxslocked_rewards"][2]-myarray[eoa]["fxslocked_rewards"][2]) +\
              max(0,myarray[-1]["crvstaked_rewards"][2]-myarray[eoa]["crvstaked_rewards"][2])+\
              max(0,myarray[-1]["fxslocked_rewards"][3][0]['amount']-myarray[eoa]["fxslocked_rewards"][3][0]['amount'])+\
              max(0,(myarray[-1]["fxslocked_rewards"][3][1]['amount']-myarray[eoa]["fxslocked_rewards"][3][1]['amount'])*myarray[-1]["FRAX"]/myarray[-1]["USDcvx"])

    diff3pool = max(0,myarray[-1]["crvstaked_rewards"][3]-myarray[eoa]["crvstaked_rewards"][3])  

    concentrator_hourly_crv, ctr_unclaimed_current, diffctr, ctr_unclaimed_tvirt = calc_concentrator_hourly(myarray,eoa,extramins,myarrayh,lookback)

    print("D$"+format((round((curveclaim_hourly + spelleth_hourly)*24*myarray[-1]['USD'], 12)), '.2f').rjust(2)+"/",end="")
    #print(format((round(cvxeth_hourly*24*myarray[-1]['USD'], 2)), '.1f').rjust(3)+"/"+Style.RESET_ALL,end="")
    print(format((round(concentrator_hourly_crv*24*myarray[-1]['USD'], 2)), '.2f').rjust(5)+"/"+Style.RESET_ALL,end="") #HACK
    print(format((round(cvxlocked_hourly*24*myarray[-1]['USD'], 12)), '.2f').rjust(2)+"/"+Style.RESET_ALL,end="")
    print(format((round(fxslocked_hourly*24*myarray[-1]['USD'], 2)), '.1f').rjust(2)+"/"+Style.RESET_ALL,end="")
    print(format((round((crvstaked_hourly + crvsquared_hourly)*24*myarray[-1]['USD'], 2)), '.0f').rjust(2)+Style.RESET_ALL,end="")

    dbuffer=f"{Fore.RED}t{Fore.WHITE}{diff3pool*24/(60+extramins)*60:>.2f}"
    dbuffer+=f"{Fore.RED}v{Fore.WHITE}{diffcrv*24/(60+extramins)*60:>.2f}"
    dbuffer+=f"{Fore.RED}a{Fore.WHITE}{diffctr*24:>5.2f}"
    dbuffer+=f"{Fore.RED}x{Fore.WHITE}{diffcvx*24/(60+extramins)*60:>.2f}"

    print(Style.DIM+"{"+dbuffer+"}"+Style.RESET_ALL,end="")
    
    cvxeth_token_price = 2 * myarray[-1]["cvxeth_rewards"][4] * ((myarray[-1]["USDcvx"] * myarray[-1]["ETH"])**(1/2))
    spelleth_token_price = 2 * myarray[-1]["spelleth_rewards"][4] * ((myarray[-1]["SPELL"] * myarray[-1]["ETH"])**(1/2))
    fxslocked_token_price = 2 * myarray[-1]["fxslocked_rewards"][4] * ((myarray[-1]["FRAX"] * (myarray[-1]["FRAX"]*myarray[-1]["fxslocked_oracle"]))**(1/2)) #hack
    crvsquared_token_price = myarray[-1]["crvsquared_rewards"][4] * ((myarray[-1]["USDcvxCRV"]*.75)+(myarray[-1]["USD"]*.25))

    print(f"{Style.DIM}[{myarray[-1]['concentrator_rewards_CTR']:4.1f}",end='')
    print(f"+{ctr_unclaimed_current:5.2f}]{Style.RESET_ALL}",end=" ") #-{ctr_unclaimed_past:5.2f}
    #print(f"{myarray[-1]['concentrator_totalmined']/1000:.0f}|${dollar_value_total_ctr_earned:.0f}",end=" ")
    
    totalvalue = ((myarray[-1]["cvxeth_rewards"][0]+(211* myarray[-1]["concentrator_x2e_virt"] ))*cvxeth_token_price)+\
                  (myarray[-1]["spelleth_rewards"][0]*spelleth_token_price)+\
                  (myarray[-1]["fxslocked_rewards"][0]*fxslocked_token_price)+\
                  (myarray[-1]["crvstaked_rewards"][0]*myarray[-1]['USDcvxCRV'])+\
                  (myarray[-1]["crvsquared_rewards"][0]*crvsquared_token_price)+\
                  (myarray[-1]["cvxlocked_rewards"][0]*myarray[-1]['USDcvx'])
    #print(f"[{totalvalue:.0f}]",end="")
    #curveclaim_hourly + 
    daily_dollar_amount = (concentrator_hourly_crv+(spelleth_hourly)+(crvstaked_hourly + cvxlocked_hourly)+cvxeth_hourly+crvsquared_hourly+fxslocked_hourly)*24*myarray[-1]['USD']
    mainpercentdisplay = daily_dollar_amount *365/totalvalue *100

    return daily_dollar_amount, mainpercentdisplay,diffcrv*24/(60+extramins)*60,diffctr*24

def print_status_line(carray, myarray, myarrayh, eoa, w3, lookback):
    """print main status line"""
    extramins = round((myarray[-1]["raw_time"]-myarray[eoa]["raw_time"])/60)+eoa+1
    cvxeth_token_price = 2 * myarray[-1]["cvxeth_rewards"][4] * ((myarray[-1]["USDcvx"] * myarray[-1]["ETH"])**(1/2))
    #spelleth_token_price = 2 * myarray[-1]["spelleth_rewards"][4] * ((myarray[-1]["SPELL"] * myarray[-1]["ETH"])**(1/2))
    fxslocked_token_price = 2 * myarray[-1]["fxslocked_rewards"][4] * ((myarray[-1]["FRAX"] * (myarray[-1]["FRAX"]*myarray[-1]["fxslocked_oracle"]))**(1/2)) #hack
    #tripool_token_price =  3 * ((myarray[-1]["BTC"] * myarray[-1]["ETH"])**(1/3))
    #tripool_value_modifyer = tripool_token_price / 1229
    crvsquared_token_price = myarray[-1]["crvsquared_rewards"][4] * ((myarray[-1]["USDcvxCRV"]*.75)+(myarray[-1]["USD"]*.25))

    #Start line with time and price information
    print("\r",end='',flush=True)
    print(myarray[-1]["human_time"], end=' - ')

    #show daily differnce calculations   
    daily_dollar_amount, mainpercentdisplay,crv_hourly,cvx_hourly = show_difference(myarray,eoa,myarrayh,lookback)

    #show vestiges of raw tri-pool (non-convex) ecosystem
    #curve_functions.curve_boost_check(carray, w3)
    #print("["+Fore.BLUE+f"{100*round(tripool_value_modifyer-1,2):2.0f}"+Style.RESET_ALL+"%]", end=' ')
    show_curve(carray, myarray, myarrayh, eoa, extramins, lookback, True)
    show_abra(myarray, eoa, extramins, True)

    #show profitability percentages for each convex contract
    #show_convex2_extracvx(myarray, eoa,extramins,"concentrator_cvxeth_rewards","xX2E", 0, cvxeth_token_price, myarrayh,lookback,"",True,"") #Indicates no third pool and using token_value_modifyer

    concentrator_hourly_crv, ctr_unclaimed_current, diffctr, ctr_unclaimed_tvirt = calc_concentrator_hourly(myarray,eoa,extramins,myarrayh,lookback)
    print(Fore.RED+Style.BRIGHT+"cX2E"+Style.RESET_ALL+Fore.WHITE+f"{(ctr_unclaimed_tvirt+(concentrator_hourly_crv*24*myarray[-1]['USD'] *365/(211* myarray[-1]['concentrator_x2e_virt'] *cvxeth_token_price)))*100:5.2f}",end=" ")

    #CONCENTRATOR_FEE = 1
    #diffconcvirtw = max(0,myarray[-1]["concentrator_virt"]-myarrayh[-(24*7)-1]["concentrator_virt"])*365/7 *CONCENTRATOR_FEE#* 24/(lookback+float(int(minut)/60))
    #diffconcvirt5 = max(0,myarray[-1]["concentrator_virt"]-myarrayh[-(24*5)-1]["concentrator_virt"])*365/5 *CONCENTRATOR_FEE#* 24/(lookback+float(int(minut)/60))
    #diffconcvirt3 = max(0,myarray[-1]["concentrator_virt"]-myarrayh[-(24*14)-1]["concentrator_virt"])*365/14 *CONCENTRATOR_FEE#* 24/(lookback+float(int(minut)/60))
    #diffconcvirtd = max(0,myarray[-1]["concentrator_virt"]-myarrayh[-(24*1)-1]["concentrator_virt"])*365/1 *CONCENTRATOR_FEE#* 24/(lookback+float(int(minut)/60))
    #print(f"{Style.DIM}{{{diffconcvirtd * 100:5.2f}/{diffconcvirt3 * 100:5.2f}/{diffconcvirt5 * 100:5.2f}/{diffconcvirtw * 100:5.2f}}}{Style.RESET_ALL}", end=" ")

    show_cvxlocked_rewards(myarray, eoa, extramins,True)
    show_convex2_extrafxs(myarray, eoa,extramins,"fxslocked_rewards","xFXS", 0, fxslocked_token_price,myarrayh,lookback,"",True)
    show_convex2_extracvx(myarray, eoa,extramins,"crvsquared_rewards","xV2V", 0, crvsquared_token_price, myarrayh,lookback,"",True,"") #Indicates no third pool and using token_value_modifyer
    show_convex(myarray, eoa,extramins,"crvstaked_rewards","xCRV", 1, 1,True) #Indicates having an extra 3pool and not using token_value_modifyer
    #show crv / cvxcrv price differential
    print(f"[{Fore.CYAN}{Style.BRIGHT}{(myarray[-1]['USDcvxCRV'] - myarray[-1]['USD']) / myarray[-1]['USD'] * 100:4.1f}/{myarray[-1]['crvsquared_balances']*100:4.1f}{Style.RESET_ALL}%]", end="")
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
