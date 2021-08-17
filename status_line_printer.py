#!/usr/bin/env python3
"""curve"""
# pylint: disable=C0103,C0301,W0105,E0401,R0914,C0411,W0702,C0200,C0116,w0106
import time
from colorama import Fore, Style
import curve_functions
import tripool_calc
from tools.ens_helper import ipfs_hash_value

curve_ipfs_current_hash="Qmap8m62DnovFjN7jpdvbqhiBuQsipux2gEKLFjQmiNrqB"

def show_convex(carray, myarray, eoa, extramins, name, label, extrapools, tokenmodindex):
    """cvx display"""
    labels = [ "I", "v", "x", "t"]
    pricefactor = [ carray["token_value_modifyer"][tokenmodindex], myarray[-1]["USD"], myarray[-1]["USDcvx"], myarray[-1]["USD3pool"]]
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
        subtotal=str(format(round(tprofit/((myarray[eoa][name][0]+.000000001)*pricefactor[extrapools])*100, 2), '5.2f')).rjust(5)

    print(Fore.RED+Style.BRIGHT+label+Style.RESET_ALL+subtotal+Style.DIM+"{"+buffer+"}"+Style.RESET_ALL, end=' ')

def show_cvx_rewards(myarray, eoa, extramins):
    """cvx staking rewards display"""
    try:
        tprofit=(myarray[-1]["cvxcrv_rewards"][1]-myarray[eoa]["cvxcrv_rewards"][1])/(60+extramins)*myarray[-1]["USDcvxCRV"]*60*24*365
        subtotal=str(format(round(tprofit/(myarray[eoa]["cvxcrv_rewards"][0]*myarray[-1]["USDcvx"])*100, 2), '5.2f')).rjust(5)
    except Exception:
        subtotal="xx.xx"

    print(Fore.RED+Style.BRIGHT+"xCVX"+Style.RESET_ALL+subtotal, end=' ')

def show_cvxsushi_rewards(myarray, eoa, extramins):
    """cvx sushi rewards display"""
    cvxsushi_token_modifyer = 270 # HACK
    try:
        tprofit=(myarray[-1]["cvxsushi_rewards"][1]-myarray[eoa]["cvxsushi_rewards"][1])/(60+extramins)*myarray[-1]["USDcvx"]*60*24*365
        subtotal=str(format(round(tprofit/(myarray[-1]["cvxsushi_rewards"][0]*cvxsushi_token_modifyer)*100, 2), '5.2f')).rjust(5)
    except Exception:
        subtotal="xx.xx"

    print(Fore.RED+Style.BRIGHT+"sCVX"+Style.RESET_ALL+subtotal, end=' ')

def show_curve(carray, myarray, myarrayh, eoa, extramins, USD, lookback):
    tprofit = 0
    buffer = ""
    _, _, _, minut = map(str, time.strftime("%m %d %H %M").split())
    for i in range(0, len(carray["name"])):
        if carray["currentboost"][i] > 0:
            buffer+=Fore.RED+Style.BRIGHT+carray["name"][i]+Style.RESET_ALL
            try:
                buffer+=str(format(round((myarray[-1][carray["name"][i]+"pool"]-myarray[eoa][carray["name"][i]+"pool"])/(60+extramins)*60*USD*24*365/carray["invested"][i]*100, 2), '.2f')).rjust(5)[0:5]
            except Exception:
                buffer+="xx.xx"
            try:
                thisdiff = (myarray[-1][carray["name"][i]+"profit"]-myarrayh[-lookback-1][carray["name"][i]+"profit"])/(lookback+float(int(minut)/60))
            except Exception:
                thisdiff = -1

            if thisdiff >= 0:
                tprofit += thisdiff
                buffer += Style.DIM+Fore.GREEN+str(format(round(thisdiff/60*60*USD*24*365/carray["invested"][i]*100, 2), '.2f')).rjust(5)[0:5]+" "+Style.RESET_ALL
            else:
                buffer += Style.DIM+Fore.GREEN+"xx.xx "+Style.RESET_ALL

    return tprofit, buffer

def print_status_line(carray, myarray, myarrayh, USD, eoa, w3, lookback):
    """print main status line"""
    extramins = round((myarray[-1]["raw_time"]-myarray[eoa]["raw_time"])/60)+eoa
    diffa = max(0,(myarray[-1]["claim"]-myarray[eoa]["claim"]))
    diffb = max(0,myarray[-1]["trix_rewards"][1]-myarray[eoa]["trix_rewards"][1]+((myarray[-1]["trix_rewards"][2]-myarray[eoa]["trix_rewards"][2])*myarray[-1]["USDcvx"]/myarray[-1]["USD"]))
    difference = (diffa + diffb) / (60+extramins)*60
    print("\r",end='',flush=True)
    print(myarray[-1]["human_time"], end=' ')
    print("$"+Fore.YELLOW+Style.BRIGHT+f"{USD:5.2f}"+Style.RESET_ALL, end=' ') #csym+"1"+Style.RESET_ALL+" = "+
    print("$"+Fore.YELLOW+f"{myarray[-1]['USDcvx']:5.2f}"+Style.RESET_ALL,end=" - ", flush=True)

    tprofit, buffer = show_curve(carray, myarray, myarrayh, eoa, extramins, USD, lookback)
    print(Fore.GREEN+Style.BRIGHT+str(format(round((difference)*USD*24*365/(sum(carray["invested"])+(myarray[-1]["trix_rewards"][0]*carray["token_value_modifyer"][carray["longname"].index("tRicrypto")]))*100, 2), '5.2f'))+Style.RESET_ALL+"/", end='')
    print(Fore.YELLOW+str(format(round((tprofit/60*60)*24*365/sum(carray["invested"])*100, 2), '5.2f'))[0:5]+Style.RESET_ALL+"% APR", end=' - ')
    print("D$"+format((round(difference*24*myarray[-1]['USD'], 2)), '.2f').rjust(5)+Style.RESET_ALL,end=" ")
    print('-',buffer, end='')
    #print("H"+csym+format((round(difference, 5)), '.4f')+Style.RESET_ALL, end=' ')
    #print("D"+csym+format((round(difference*24, 2)), '.2f').rjust(5)+Style.RESET_ALL+
    #      "/$"+Fore.YELLOW+f"{round(24*tprofit,2):5.2f}"+Style.RESET_ALL, end= ' ')
    #print("Y"+csym+format((round(difference*24*365, 0)), '.0f').rjust(4)+Style.RESET_ALL+
    #      "/$"+Fore.YELLOW+str(format(round(24*365*tprofit,2), '.0f')).rjust(4)+Style.RESET_ALL, end=' ')
    print('[', end='')
    curve_functions.curve_boost_check(carray, w3)
    print('\b] ', end='')
    show_convex(carray, myarray, eoa,extramins,"trix_rewards","xTri", 0, carray["longname"].index("tRicrypto")) #Indicates no third pool and using token_value_modifyer
    tripool_calc.tri_calc(False,-1)
    show_convex(carray, myarray, eoa,extramins,"cvx_rewards","xCRV", 1, 0) #Indicates having an extra 3pool and not using token_value_modifyer
    print("["+Fore.CYAN+Style.BRIGHT+f"{((myarray[-1]['USDcvxCRV']-myarray[-1]['USD'])/myarray[-1]['USD'])*100:5.2f}"+Style.RESET_ALL+"%]",end=" ")
    #print("$"+Fore.YELLOW+Style.BRIGHT+f"{myarray[-1]['USDcvxCRV']:.2f}"+Style.RESET_ALL,end=" ")
    show_cvx_rewards(myarray, eoa, extramins)
    show_cvxsushi_rewards(myarray, eoa, extramins)
    if extramins >= 0: #air bubble extra minutes
        print(Fore.RED+str(round((myarray[-1]["raw_time"]-myarray[eoa]["raw_time"])/60)+eoa+1)+Style.RESET_ALL, end=' ')
    if eoa > -61:  #fewer than 60 records in the ghistory.json file
        print(Fore.RED+Style.BRIGHT+str(61+eoa).rjust(2)+Style.RESET_ALL, end=' ')
    if myarray[-1]["invested"] != myarray[eoa]["invested"]:
        print(Fore.RED+str(round(myarray[-1]["invested"] - myarray[eoa]["invested"]))+Style.RESET_ALL, end=' ')
    if myarray[-1]["cvx_rewards"][0] != myarray[eoa]["cvx_rewards"][0]:
        print(Fore.RED+str(round(myarray[-1]["cvx_rewards"][0] - myarray[eoa]["cvx_rewards"][0]))+Style.RESET_ALL, end=' ')
    if myarray[-1]["trix_rewards"][0] != myarray[eoa]["trix_rewards"][0]:
        print(Fore.RED+str(round(myarray[-1]["trix_rewards"][0] - myarray[eoa]["trix_rewards"][0]))+Style.RESET_ALL, end=' ')
    if myarray[-1]["cvxcrv_rewards"][0] != myarray[eoa]["cvxcrv_rewards"][0]:
        print(Fore.RED+str(round(myarray[-1]["cvxcrv_rewards"][0] - myarray[eoa]["cvxcrv_rewards"][0]))+Style.RESET_ALL, end=' ')
    try:  #check to see if the interface linked on ipfs has changed
        if ipfs_hash_value(w3, 'curve.eth') != curve_ipfs_current_hash:
            print(Fore.RED+Style.BRIGHT+"WW"+Style.RESET_ALL, end=' ')
        else:
            print("W", end=' ')
    except:
        print(Fore.WHITE+Style.DIM+"w"+Style.RESET_ALL, end=' ')


    return round(((difference*myarray[-1]["USD"])+(tprofit/60*60))*24*365/(sum(carray["invested"])+(myarray[-1]["trix_rewards"][0]*carray["token_value_modifyer"][carray["longname"].index("tRicrypto")]))*100, 2) #display_percent

if __name__ == "__main__":
    print("this module is not meant to be run solo")
