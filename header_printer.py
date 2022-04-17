import time
from colorama import Fore, Style
from tools.load_contract import load_contract, call_me
import status_line_printer

MY_WALLET_ADDRESS = "0x8D82Fef0d77d79e5231AE7BFcFeBA2bAcF127E2B"

def convex_header_display(myarray,myarrayh,lookback):

    trix_value = ((myarray[-1]["trix_rewards"][2]*myarray[-1]["USDcvx"])+
                  (myarray[-1]["trix_rewards"][1]*myarray[-1]["USD"]))

    mimx_value = ((myarray[-1]["mimx_rewards"][2]*myarray[-1]["USDcvx"])+
                  (myarray[-1]["mimx_rewards"][1]*myarray[-1]["USD"]))

    crveth_value = ((myarray[-1]["crveth_rewards"][2]*myarray[-1]["USDcvx"])+
                  (myarray[-1]["crveth_rewards"][1]*myarray[-1]["USD"]))

    cvxeth_value = ((myarray[-1]["cvxeth_rewards"][2]*myarray[-1]["USDcvx"])+
                  (myarray[-1]["cvxeth_rewards"][1]*myarray[-1]["USD"])+
                  (myarray[-1]["cvxeth_extracvx"]*myarray[-1]["USDcvx"]))

    fxslocked_value = ((myarray[-1]["fxslocked_rewards"][2]*myarray[-1]["USDcvx"])+
                  (myarray[-1]["fxslocked_rewards"][1]*myarray[-1]["USD"])+
                  (myarray[-1]["fxslocked_extracvx"]*myarray[-1]["USDcvx"])+
                  (myarray[-1]["fxslocked_extrafxs"]*myarray[-1]["FRAX"]))

    spelleth_value = ((myarray[-1]["spelleth_rewards"][2]*myarray[-1]["USDcvx"])+
                  (myarray[-1]["spelleth_rewards"][1]*myarray[-1]["USD"]))

    crvstaked_value = ((myarray[-1]["crvstaked_rewards"][3]*myarray[-1]["USD3pool"])+
                 (myarray[-1]["crvstaked_rewards"][2]*myarray[-1]["USDcvx"])+
                 (myarray[-1]["crvstaked_rewards"][1]*myarray[-1]["USD"]))

    cvxlocked_value = (myarray[-1]["cvxlocked_rewards"][1]*myarray[-1]["USDcvxCRV"])

    tripool_token_price =  3 * ((myarray[-1]["BTC"] * myarray[-1]["ETH"])**(1/3))
    crveth_token_price = 2 * myarray[-1]["crveth_virt"] * ((myarray[-1]["USD"] * myarray[-1]["ETH"])**(1/2))
    cvxeth_token_price = 2 * myarray[-1]["cvxeth_virt"] * ((myarray[-1]["USDcvx"] * myarray[-1]["ETH"])**(1/2))
    spelleth_token_price = 2 * myarray[-1]["spelleth_virt"] * ((myarray[-1]["SPELL"] * myarray[-1]["ETH"])**(1/2))
    fxslocked_token_price = 2 * myarray[-1]["fxslocked_virt"] * ((myarray[-1]["FRAX"] * (myarray[-1]["FRAX"]*myarray[-1]["fxslocked_oracle"]))**(1/2)) #hack

    crv_crv_owned = myarray[-1]["crveth_rewards"][0]*crveth_token_price / 2 / myarray[-1]["USD"]
    crv_eth_owned = myarray[-1]["crveth_rewards"][0]*crveth_token_price / 2 / myarray[-1]["ETH"]

    cvx_cvx_owned = myarray[-1]["cvxeth_rewards"][0]*cvxeth_token_price / 2 / myarray[-1]["USDcvx"]
    cvx_eth_owned = myarray[-1]["cvxeth_rewards"][0]*cvxeth_token_price / 2 / myarray[-1]["ETH"]

    spell_spell_owned = myarray[-1]["spelleth_rewards"][0]*spelleth_token_price / 2 / myarray[-1]["SPELL"]
    spell_eth_owned = myarray[-1]["spelleth_rewards"][0]*spelleth_token_price / 2 / myarray[-1]["ETH"]

    #crveth_imploss = round(100 * ( (myarray[-1]["crveth_rewards"][0]*crveth_token_price) - ((27*tripool_token_price)+(4.47*myarray[-1]["ETH"])))/(myarray[-1]["crveth_rewards"][0]*crveth_token_price),2)
    cvxeth_imploss = round(100 * ( (myarray[-1]["cvxeth_rewards"][0]*cvxeth_token_price) - ((1884*myarray[-1]["USDcvx"])+((5.714+14)*myarray[-1]["ETH"])))/(myarray[-1]["cvxeth_rewards"][0]*cvxeth_token_price),2)
    cvxeth_implossa = round(100 * ( (105*cvxeth_token_price) - ((1884*myarray[-1]["USDcvx"])+((5.714)*myarray[-1]["ETH"])))/(105*cvxeth_token_price),2)
    cvxeth_implossb = round(100 * ( (59*cvxeth_token_price) - (14*myarray[-1]["ETH"]))/(59*cvxeth_token_price),2)
    cvxeth_implossaraw =  round((105*cvxeth_token_price) - ((1884*myarray[-1]["USDcvx"])+((5.714)*myarray[-1]["ETH"])))
    cvxeth_implossbraw =  round((59*cvxeth_token_price) - (14*myarray[-1]["ETH"]))

    spelleth_imploss = round(100 * ( (myarray[-1]["spelleth_rewards"][0]*spelleth_token_price) - 6400)/(myarray[-1]["spelleth_rewards"][0]*spelleth_token_price),2)
    frax_imploss = round((140*myarray[-1]["FRAX"]) - 3000)

    #duplicate code begin
    eoa = 0 - len(myarray)
    extramins = round((myarray[-1]["raw_time"]-myarray[eoa]["raw_time"])/60)+eoa
    diffh = max(0.0001,myarray[-1]["spelleth_rewards"][1]-myarray[eoa]["spelleth_rewards"][1]\
                +((myarray[-1]["spelleth_rewards"][2]-myarray[eoa]["spelleth_rewards"][2])*myarray[-1]["USDcvx"]/myarray[-1]["USD"]))
    difference_spelleth = diffh / (60+extramins)*60

    cvxeth_daily = max(0.0001,myarray[-1]["cvxeth_rewards"][1]-myarray[eoa]["cvxeth_rewards"][1]\
                +((myarray[-1]["cvxeth_rewards"][2]-myarray[eoa]["cvxeth_rewards"][2])*myarray[-1]["USDcvx"]/myarray[-1]["USD"])\
                +((myarray[-1]["cvxeth_extracvx"]-myarray[eoa]["cvxeth_extracvx"])*myarray[-1]["USDcvx"]/myarray[-1]["USD"])\
                / (60+extramins)*60)   

    crveth_daily = max(0.0001,myarray[-1]["crveth_rewards"][1]-myarray[eoa]["crveth_rewards"][1]\
                +((myarray[-1]["crveth_rewards"][2]-myarray[eoa]["crveth_rewards"][2])*myarray[-1]["USDcvx"]/myarray[-1]["USD"])\
                / (60+extramins)*60)
    fxslocked_daily = max(0.0001,myarray[-1]["fxslocked_rewards"][1]-myarray[eoa]["fxslocked_rewards"][1]\
                +((myarray[-1]["fxslocked_rewards"][2]-myarray[eoa]["fxslocked_rewards"][2])*myarray[-1]["USDcvx"]/myarray[-1]["USD"])\
                +((myarray[-1]["fxslocked_extracvx"]-myarray[eoa]["fxslocked_extracvx"])*myarray[-1]["USDcvx"]/myarray[-1]["USD"])\
                +((myarray[-1]["fxslocked_extrafxs"]-myarray[eoa]["fxslocked_extrafxs"])*myarray[-1]["FRAX"]/myarray[-1]["USD"]))\
                / (60+extramins)*60
    #duplicate code end
    fudgefactor = 3/4  #because we entered the pool when cvx was so low, we will never get close to even unless we pretend we entered with less cvx initailly
    #crv = eth / 625 for break even 
    days_of_imp_crv =  ( ((27*tripool_token_price)+(4.47*myarray[-1]["ETH"])) - (myarray[-1]["crveth_rewards"][0]*crveth_token_price) ) / (crveth_daily *24*myarray[-1]['USD'])
    days_of_imp_cvx =  ( ((1884*fudgefactor*myarray[-1]["USDcvx"])+((5.714+14)*myarray[-1]["ETH"])) - (myarray[-1]["cvxeth_rewards"][0]*cvxeth_token_price) ) / (cvxeth_daily *24*myarray[-1]['USD'])
    days_of_imp_spell = (6400 - (myarray[-1]["spelleth_rewards"][0]*spelleth_token_price) ) / (difference_spelleth *24*myarray[-1]['USD'])
    days_of_imp_fxs = ((4500*2) - (myarray[-1]["fxslocked_rewards"][0]*fxslocked_token_price))/ (fxslocked_daily *24*myarray[-1]['USD'])

#    print("xMim-Ust"," "*19,str(round(myarray[-1]["mimx_rewards"][0])).rjust(5),end=" ")
#    print(" "*37,(f"${mimx_value:7.2f}").rjust(8),end=" ")
#    print(" "*29,"v"+str(format(round(myarray[-1]["mimx_rewards"][1],2), '5.2f')).rjust(5)+"x"+str(format(round(myarray[-1]["mimx_rewards"][2],2), '5.2f')).rjust(5))

    print("xSpell/Eth"," "*2,Style.DIM+str(round(myarray[-1]["spelleth_rewards"][0]*spelleth_token_price)).rjust(6)+Style.RESET_ALL,end=" ")
#    print(f"({spelleth_imploss:3.0f}%/{min(days_of_imp_spell,999):3.0f}d)".ljust(11),end="")
    print(f"({min(days_of_imp_spell,999):3.0f}d)".ljust(7),end="")
    print(" "*2,f"s{spell_spell_owned/1000:3.0f}k e{spell_eth_owned:5.2f}",end='')
    print(" "*1,("$"+str(format(round(spelleth_value,2), '7.2f'))).rjust(8),end=" ")
    status_line_printer.show_convex2(myarray, eoa,extramins,"spelleth_rewards","xS2E", 0, spelleth_token_price,myarrayh,lookback,"spelleth_virt", False) #Indicates no third pool and using token_value_modifyer
    print(" "*13,"v"+str(format(round(myarray[-1]["spelleth_rewards"][1],2), '5.2f')).rjust(5)+"x"+str(format(round(myarray[-1]["spelleth_rewards"][2],2), '5.2f')).rjust(5))

    print("Staked FXS"," "*2,Style.DIM+str(round(myarray[-1]["fxslocked_rewards"][0]*fxslocked_token_price)).rjust(6)+Style.RESET_ALL,end=" ")
    if days_of_imp_fxs > 0:
        print(f"({min(days_of_imp_fxs,999):3.0f}d)".ljust(7),end="")
    else:
        print(f"( ok )".ljust(7),end="")
    print(" "*1,"xf"+str(round(myarray[-1]["fxslocked_rewards"][0]*2)).rjust(4),end=" ")
    print(" "*7,("$"+str(format(round(fxslocked_value,2), '7.2f'))).rjust(8), end=" ")
    status_line_printer.show_convex2_extrafxs(myarray, eoa,extramins,"fxslocked_rewards","xFXS", 0, fxslocked_token_price,myarrayh,lookback,"fxslocked_virt", False)
    print(" "*42,"f"+str(format(round(myarray[-1]["fxslocked_extrafxs"],2), '5.2f')).rjust(5)+"v"+str(format(round(myarray[-1]["fxslocked_rewards"][1],2), '5.2f')).rjust(5)+"x"+str(format(round(myarray[-1]["fxslocked_rewards"][2]+myarray[-1]["fxslocked_extracvx"],2), '5.2f')).rjust(5))

    #print("crV/Eth"," "*6,Style.DIM+str(round(myarray[-1]["crveth_rewards"][0]*crveth_token_price)).rjust(5)+Style.RESET_ALL,end=" ")
    #if crveth_imploss > 0:
    #    print(("("+Fore.GREEN+f"{crveth_imploss:4.1f}"+Style.RESET_ALL+"%)    ").ljust(11),end="")
    #else:
 #  #     print(f"({crveth_imploss:3.0f}%/{min(days_of_imp_crv,999):3.0f}d)".rjust(11),end=" ")
    #    print(f"({min(days_of_imp_crv,999):3.0f}d)".ljust(7),end="")
    #print(" "*2,f"v{crv_crv_owned:4.0f} e{crv_eth_owned:5.2f}",end="")
    #print(" "*1,("$"+str(format(round(crveth_value,2), '7.2f'))).rjust(8),end=" ")
    #status_line_printer.show_convex2(myarray, eoa,extramins,"crveth_rewards","xV2E", 0, crveth_token_price, myarrayh,lookback,"crveth_virt", False) #Indicates no third pool and using token_value_modifyer
    #print(" "*83,"v"+str(format(round(myarray[-1]["crveth_rewards"][1],2), '5.2f')).rjust(5)+"x"+str(format(round(myarray[-1]["crveth_rewards"][2],2), '5.2f')).rjust(5))

    print("cvX/Eth"," "*5,Style.DIM+str(round(myarray[-1]["cvxeth_rewards"][0]*cvxeth_token_price)).rjust(6)+Style.RESET_ALL,end=" ")
#    print(f"({cvxeth_imploss:3.0f}%/{min(days_of_imp_cvx,999):3.0f}d)".ljust(11),end="")
    print(f"({min(days_of_imp_cvx,999):3.0f}d)".ljust(7),end="")
    print(" "*2,f"x{cvx_cvx_owned:4.0f} e{cvx_eth_owned:5.2f}",end='')
    print(" "*1,("$"+str(format(round(cvxeth_value,2), '7.2f'))).rjust(8),end=" ")
    status_line_printer.show_convex2_extracvx(myarray, eoa,extramins,"cvxeth_rewards","xX2E", 0, cvxeth_token_price, myarrayh,lookback,"cvxeth_virt", False) #Indicates no third pool and using token_value_modifyer
    print(" "*112,"v"+str(format(round(myarray[-1]["cvxeth_rewards"][1],2), '5.2f')).rjust(5)+"x"+str(format(round(myarray[-1]["cvxeth_rewards"][2]+myarray[-1]["cvxeth_extracvx"],2), '5.2f')).rjust(5))
    #print(" "*5,f"[{cvxeth_implossa}% {cvxeth_implossb}% {cvxeth_implossaraw} {cvxeth_implossbraw}]")

    print("Staked CRV"," "*3,Style.DIM+str(round(myarray[-1]["crvstaked_rewards"][0]*myarray[-1]["USDcvxCRV"])).rjust(5)+Style.RESET_ALL,end="")
    print(" "*9,"vv"+str(myarray[-1]["crvstaked_rewards"][0]),end="")
    print(" "*8,("$"+str(format(round(crvstaked_value,2), '7.2f'))).rjust(8),end=" ")
    status_line_printer.show_convex(myarray, eoa,extramins,"crvstaked_rewards","xCRV", 1, 1, False) #Indicates having an extra 3pool and not using token_value_modifyer
    print(" "*142,"t"+str(format(round(myarray[-1]["crvstaked_rewards"][3],2), '5.2f')).rjust(5)+"v"+str(format(round(myarray[-1]["crvstaked_rewards"][1],2), '5.2f')).rjust(5)+"x"+str(format(round(myarray[-1]["crvstaked_rewards"][2],2), '5.2f')).rjust(5))

    print("Locked CVX"," "*3,Style.DIM+str(round(myarray[-1]["cvxlocked_rewards"][0]*myarray[-1]["USDcvx"])).rjust(5)+Style.RESET_ALL,end="")
    print(" "*10,"x"+str(round(myarray[-1]["cvxlocked_rewards"][0])).rjust(4),end="")
    print(" "*8,("$"+str(format(round(cvxlocked_value,2), '7.2f'))).rjust(8),end=" ")
    status_line_printer.show_cvxlocked_rewards(myarray, eoa, extramins, False)
    print(" "*164,"vv"+str(format(round(myarray[-1]["cvxlocked_rewards"][1],2), '5.2f')).rjust(5))
    
def curve_header_display(myarray, carray, w3, fullheader):
    """display detailed pool information"""
    vecrv_func = load_contract("0x5f3b5DfEb7B28CDbD7FAba78963EE202a494e2A2",w3)
    virutal_price_sum = 0
    cw = [5, 6, 11, 6, 7, 4, 0, 9, 6, 7, 5]
    veCRV_mine = round(call_me(vecrv_func.balanceOf(MY_WALLET_ADDRESS))/10**18, 2)
    veCRV_total = round(call_me(vecrv_func.totalSupply())/10**18, 2)
    for i in range(0, len(carray["name"])):
        if carray["currentboost"][i] > 0 or fullheader:
            carray["totalsupply"][i] = round(call_me(load_contract(carray["gaugeaddress"][i],w3).totalSupply())/10**18, 2)
            carray["virtprice"][i] = round(call_me(load_contract(carray["swapaddress"][i],w3).get_virtual_price())/10**18, 6)
            carray["balanceof"][i] = round(call_me(load_contract(carray["gaugeaddress"][i],w3).balanceOf(MY_WALLET_ADDRESS))/10**18, 2)
            if len(carray["tokenaddress"][i]) > 1:
                carray["balanceof"][i] += round(call_me(load_contract(carray["tokenaddress"][i],w3).balanceOf(MY_WALLET_ADDRESS))/10**18, 2)
            virutal_price_sum += carray["virtprice"][i]*carray["balanceof"][i]*carray["token_value_modifyer"][i]
            maxinvestforfullboost = carray["totalsupply"][i]*veCRV_mine/veCRV_total
            print(carray["longname"][i].ljust(len(max(carray["longname"], key=len))), carray["name"][i], end=' ')
            print(str(format(carray["totalsupply"][i], ',.0f')).rjust(cw[2]), end=' ')
            print("|", end=' ')
            if carray["invested"][i] > 0:
                print(str(carray["invested"][i]).rjust(cw[0]), end=' ')
            else:
                print(" "*cw[0], end=' ')

            if carray["virtprice"][i]*carray["balanceof"][i]*carray["token_value_modifyer"][i] > 0:
                print(Style.DIM+Fore.GREEN+str(format((carray["virtprice"][i]*carray["balanceof"][i]*carray["token_value_modifyer"][i])-carray["invested"][i], '.2f')).rjust(cw[1])+Style.RESET_ALL, end=' ')
            else:
                print(" "*cw[1], end=' ')

            base_percent = ((carray["virtprice"][i]*carray["balanceof"][i]*carray["token_value_modifyer"][i])-carray["invested"][i])/(carray["invested"][i]+.00000001)*100
            if base_percent > 0 and carray["currentboost"][i] > 0:
                print("("+str(format(round(base_percent,3), '.3f')).rjust(5)+"%)", end=' ')
            else:
                print(" "*8, end=' ')
            #needed_veCRV = round((carray["balanceof"][i]/carray["totalsupply"][i]*veCRV_total)-veCRV_mine)
            carray["futureboost"][i] = 2.5*min((carray["balanceof"][i]/2.5) + (maxinvestforfullboost*(1-(1/2.5))), carray["balanceof"][i])/max(1,carray["balanceof"][i])
            #print(Style.DIM+str(format(round(carray["minted"][i]/10**18, 2), '.2f')).rjust(cw[4])+Style.RESET_ALL, end=' ')
            print("|", end=' ')
            if carray["currentboost"][i] >= 2.47:
                if carray["futureboost"][i]-carray["currentboost"][i] < 0:
                    #print(Style.DIM+Fore.GREEN+str(format(abs(round(maxinvestforfullboost-carray["balanceof"][i], 2)), '.2f')).rjust(cw[7])+Style.RESET_ALL, end=' ')
                    print(Style.BRIGHT+Fore.GREEN+str(format(carray["currentboost"][i], '.4f')).rjust(cw[8]).replace("0", " ")+Style.RESET_ALL, end=' ')
                    print(Style.DIM+Fore.GREEN+str(format(carray["futureboost"][i]-carray["currentboost"][i], '.4f')).rjust(cw[9])+Style.RESET_ALL, end=' ')
                    #print(Style.DIM+str(needed_veCRV).rjust(cw[10]), "additional veCRV needed to maintain full boost."+Style.RESET_ALL)
                    print("")
                else:
                    print(Style.BRIGHT+Fore.GREEN+str(format(carray["currentboost"][i], '.4f')).rjust(cw[8]).replace("0", " ")+Style.RESET_ALL, end=' ')
                    #print(" "*cw[9], end=' ')
                    print(("$"+str(format((maxinvestforfullboost-carray["balanceof"][i])*carray["token_value_modifyer"][i], '.0f'))).ljust(5)+Style.RESET_ALL, "fits   ", end='')
            elif carray["currentboost"][i] > 0:
                #print(Style.DIM+str(format(round(maxinvestforfullboost-carray["balanceof"][i], 2), '.2f')).rjust(cw[7])+Style.RESET_ALL, end=' ')
                print(str(format(carray["currentboost"][i], '.4f')).rjust(cw[8]), end=' ')
                if carray["futureboost"][i]-carray["currentboost"][i] <= 0:
                    print(Style.DIM+Fore.GREEN+str(format(carray["futureboost"][i]-carray["currentboost"][i], '.4f')).rjust(cw[9])+Style.RESET_ALL, end=' ')
                elif carray["futureboost"][i]-carray["currentboost"][i] < 0.05:
                    print(Style.DIM+Fore.RED+str(format(carray["futureboost"][i]-carray["currentboost"][i], '.4f')).rjust(cw[9])+Style.RESET_ALL, end=' ')
                else:
                    print(Style.BRIGHT+Fore.RED+str(format(carray["futureboost"][i]-carray["currentboost"][i], '.4f')).rjust(cw[9])+Style.RESET_ALL, end=' ')
                #print(Style.DIM+str(needed_veCRV).rjust(cw[10]), "additional veCRV needed for full boost."+Style.RESET_ALL)
                print("   ",end='')
#            print("|", end=' ')
#            print(str(format(round(myarray[-1][carray["name"][i]+"pool"], 2), '.0f')).rjust(cw[5]), end=' ')
            #print(" "*7, end='')
            if abs(round(myarray[-1][carray["name"][i]+"pool"]-round(carray["minted"][i]/10**18,2), 2)) > 0.05:
                print("$"+str(format(round((myarray[-1][carray["name"][i]+"pool"]-(round(carray["minted"][i]/10**18,2)))*myarray[-1]["USD"], 2), '7.2f')).rjust(6)+Style.RESET_ALL, end='')
                print(str("   v"+format(round(myarray[-1][carray["name"][i]+"pool"]-(round(carray["minted"][i]/10**18,2)), 2), '5.2f')).rjust(cw[3])+Style.RESET_ALL, end=' ')
            else:
                print(" "*cw[3], end=' ')
            print("")
    return virutal_price_sum

def curve_header_display2(myarray, carray, w3, fullheader,myarrayh,lookback):
    """display detailed pool information"""
    for i in range(0, len(carray["name"])):
        if carray["currentboost"][i] > 0 or fullheader:
            carray["totalsupply"][i] = round(call_me(load_contract(carray["gaugeaddress"][i],w3).totalSupply())/10**18, 2)
            carray["virtprice"][i] = round(call_me(load_contract(carray["swapaddress"][i],w3).get_virtual_price())/10**18, 6)
            carray["balanceof"][i] = round(call_me(load_contract(carray["gaugeaddress"][i],w3).balanceOf(MY_WALLET_ADDRESS))/10**18, 2)
            if len(carray["tokenaddress"][i]) > 1:
                carray["balanceof"][i] += round(call_me(load_contract(carray["tokenaddress"][i],w3).balanceOf(MY_WALLET_ADDRESS))/10**18, 2)

            print(carray["longname"][i].ljust(len(max(carray["longname"], key=len))), end='')
            print(" "*3,Style.DIM+str(format((carray["virtprice"][i]*carray["balanceof"][i]*carray["token_value_modifyer"][i]), '.0f')).rjust(4)+Style.RESET_ALL, end='')
            if abs(round(myarray[-1][carray["name"][i]+"pool"]-round(carray["minted"][i]/10**18,2), 2)) > 0.05:
                print(" "*24,"$"+str(format(round((myarray[-1][carray["name"][i]+"pool"]-(round(carray["minted"][i]/10**18,2)))*myarray[-1]["USD"], 2), '7.2f')).rjust(6)+Style.RESET_ALL, end=' ')
                eoa = 0 - len(myarray)
                extramins = round((myarray[-1]["raw_time"]-myarray[eoa]["raw_time"])/60)+eoa
                status_line_printer.show_curve(carray, myarray, myarrayh, eoa, extramins, lookback, False)
                print(" "*13,str("v"+format(round(myarray[-1][carray["name"][i]+"pool"]-(round(carray["minted"][i]/10**18,2)), 2), '5.2f')).rjust(6)+Style.RESET_ALL, end=' ')
            
            print("") 

def combined_stats_display(myarray, carray, w3):
    crv_func = load_contract("0xD533a949740bb3306d119CC777fa900bA034cd52",w3)
    vecrv_func = load_contract("0x5f3b5DfEb7B28CDbD7FAba78963EE202a494e2A2",w3)
    cvx_token = load_contract("0x4e3FBD56CD56c3e72c1403e103b45Db9da5B9D2B",w3)
    cvxcrv_token = load_contract("0x62B9c7356A2Dc64a1969e19C23e4f579F9810Aa7",w3)
    crv3pool_token = load_contract("0x6c3F90f043a72FA612cbac8115EE7e52BDe6E490",w3)
    fxslocked_token = load_contract("0xFEEf77d3f69374f66429C91d732A244f074bdf74",w3)
    fxs_token = load_contract("0x3432B6A60D23Ca0dFCa7761B7ab56459D9C964D0",w3)

    CRV_inwallet = round(call_me(crv_func.balanceOf(MY_WALLET_ADDRESS))/10**18)
    cvx_inwallet = round(call_me(cvx_token.balanceOf(MY_WALLET_ADDRESS))/10**18)
    cvxcrv_inwallet = round(call_me(cvxcrv_token.balanceOf(MY_WALLET_ADDRESS))/10**18)
    crv3pool_inwallet = round(call_me(crv3pool_token.balanceOf(MY_WALLET_ADDRESS))/10**18)
    fxslocked_inwallet = round(call_me(fxslocked_token.balanceOf(MY_WALLET_ADDRESS))/10**18,1)
    fxs_inwallet = round(call_me(fxs_token.balanceOf(MY_WALLET_ADDRESS))/10**18,1)
    veCRV_mine = round(call_me(vecrv_func.balanceOf(MY_WALLET_ADDRESS))/10**18)
    veCRV_locked = round(call_me(vecrv_func.locked(MY_WALLET_ADDRESS),expecting_list=True)/10**18)
   
    x_claimable = (myarray[-1]["crvstaked_rewards"][3]*(myarray[-1]["USD3pool"]/myarray[-1]["USD"]))+\
                  (myarray[-1]["crvstaked_rewards"][2]*(myarray[-1]["USDcvx"]/myarray[-1]["USD"]))+\
                  myarray[-1]["crvstaked_rewards"][1]+\
                  (myarray[-1]["trix_rewards"][2]*(myarray[-1]["USDcvx"]/myarray[-1]["USD"]))+\
                  myarray[-1]["trix_rewards"][1]+\
                  (myarray[-1]["mimx_rewards"][2]*(myarray[-1]["USDcvx"]/myarray[-1]["USD"]))+\
                  myarray[-1]["mimx_rewards"][1]+\
                  (myarray[-1]["crveth_rewards"][2]*(myarray[-1]["USDcvx"]/myarray[-1]["USD"]))+\
                  myarray[-1]["crveth_rewards"][1]+\
                  (myarray[-1]["spelleth_rewards"][2]*(myarray[-1]["USDcvx"]/myarray[-1]["USD"]))+\
                  myarray[-1]["spelleth_rewards"][1]+\
                  (myarray[-1]["cvxeth_rewards"][2]*(myarray[-1]["USDcvx"]/myarray[-1]["USD"]))+\
                  (myarray[-1]["cvxeth_extracvx"]*(myarray[-1]["USDcvx"]/myarray[-1]["USD"]))+\
                  myarray[-1]["cvxeth_rewards"][1]+\
                  myarray[-1]["cvxlocked_rewards"][1]+\
                 ((myarray[-1]["fxslocked_rewards"][2]*myarray[-1]["USDcvx"]/myarray[-1]["USD"])+
                  (myarray[-1]["fxslocked_rewards"][1]*myarray[-1]["USD"])+
                  (myarray[-1]["fxslocked_extracvx"]*myarray[-1]["USDcvx"]/myarray[-1]["USD"])+
                  (myarray[-1]["fxslocked_extrafxs"]*myarray[-1]["FRAX"])/myarray[-1]["USD"])
    #print("$"+str(round(sum(carray["invested"])+myarray[-1]["mimx_rewards"][0]+(myarray[-1]["trix_rewards"][0]*carray["token_value_modifyer"][carray["longname"].index("tRicrypto")]))), "invested,",sum(carray["invested"]),"is now",int(virutal_price_sum), end=' ')
    #print("("+str(format(round(( virutal_price_sum/sum(carray["invested"])*100)-100,5),'.3f'))+"%)", end='')
    print("veCRV          ",Style.DIM+str(veCRV_mine)+Style.RESET_ALL,"          Ç"+str(round(veCRV_locked)),  end='')
    print(" "*8,("$"+str(format(round((myarray[-1]["claim"]-(sum(carray["minted"])/10**18)+x_claimable)*myarray[-1]["USD"], 2),'7.2f'))).rjust(8),end ="")  
    print(Style.DIM+" {"+Fore.RED+"v"+Fore.WHITE+str(round(myarray[-1]["claim"]-(sum(carray["minted"])/10**18))+round(myarray[-1]["crvstaked_rewards"][1]+myarray[-1]["spelleth_rewards"][1]+myarray[-1]["trix_rewards"][1]+myarray[-1]["mimx_rewards"][1]+myarray[-1]["crveth_rewards"][1]+myarray[-1]["cvxeth_rewards"][1]+myarray[-1]["cvxlocked_rewards"][1]+myarray[-1]["fxslocked_rewards"][1])),end=" ")
    print(Fore.RED+"x"+Fore.WHITE+str(round(myarray[-1]["crvstaked_rewards"][2]+myarray[-1]["trix_rewards"][2]+myarray[-1]["mimx_rewards"][2]+myarray[-1]["crveth_rewards"][2]+myarray[-1]["cvxeth_rewards"][2]+myarray[-1]["spelleth_rewards"][2]+myarray[-1]["fxslocked_rewards"][2]+myarray[-1]["fxslocked_extracvx"] + myarray[-1]["cvxeth_extracvx"])),end=" ")
    print(Fore.RED+"t"+Fore.WHITE+str(round(myarray[-1]["crvstaked_rewards"][3])),end=' ')
    print(Fore.RED+"f"+Fore.WHITE+str(round(myarray[-1]["fxslocked_extrafxs"]))+"}"+Style.RESET_ALL+" to claim     ",end=' ')
    show_wallet(myarray,CRV_inwallet, cvxcrv_inwallet, cvx_inwallet, crv3pool_inwallet,fxslocked_inwallet,fxs_inwallet)

    eoa = 0 - len(myarray)
    if round((round(time.time())-myarray[eoa]["raw_time"])/60, 2)+eoa >= 0.5:
        print(Fore.RED+str(round(((round(time.time())-myarray[eoa]["raw_time"])/60)+eoa, 2))+Style.RESET_ALL+"oos", end=' ')
    if eoa > -61:
        print(Style.BRIGHT+Fore.RED+str(61+eoa)+Style.RESET_ALL+" minutes under 60.", end=' ')
    if sum(carray["invested"]) != myarray[eoa]["invested"]:
        print(Fore.RED+str(sum(carray["invested"]) - myarray[eoa]["invested"])+Style.RESET_ALL+" of New $ obs. data", end='')
    if myarray[-1]["crvstaked_rewards"][0] != myarray[eoa]["crvstaked_rewards"][0]:
        print(Fore.RED+str(myarray[-1]["crvstaked_rewards"][0] - myarray[eoa]["crvstaked_rewards"][0])+Style.RESET_ALL+" of New $ obs. data", end=' ')
    if myarray[-1]["trix_rewards"][0] != myarray[eoa]["trix_rewards"][0]:
        print(Fore.RED+str(myarray[-1]["trix_rewards"][0] - myarray[eoa]["trix_rewards"][0])+Style.RESET_ALL+" of New $ obs. data", end=' ')
    if myarray[-1]["mimx_rewards"][0] != myarray[eoa]["mimx_rewards"][0]:
        print(Fore.RED+str(myarray[-1]["mimx_rewards"][0] - myarray[eoa]["mimx_rewards"][0])+Style.RESET_ALL+" of New $ obs. data", end=' ')
    if myarray[-1]["crveth_rewards"][0] != myarray[eoa]["crveth_rewards"][0]:
        print(Fore.RED+str(myarray[-1]["crveth_rewards"][0] - myarray[eoa]["crveth_rewards"][0])+Style.RESET_ALL+" of New $ obs. data", end=' ')

    print("")

def show_wallet(myarray,CRV_inwallet,cvxcrv_inwallet,cvx_inwallet,crv3pool_inwallet,fxslocked_inwallet,fxs_inwallet):
    total = 0
    print("[", end=' ')
    if CRV_inwallet > 0:
        print("v"+Fore.CYAN+f"{CRV_inwallet}"+Style.RESET_ALL, end=' ')
        total += CRV_inwallet * myarray[-1]["USD"]
    if cvxcrv_inwallet > 0:
        print("vv"+Fore.CYAN+f"{cvxcrv_inwallet}"+Style.RESET_ALL, end=' ')
        total += cvxcrv_inwallet * myarray[-1]["USDcvxCRV"]
    if cvx_inwallet > 0:
        print("x"+Fore.BLUE+f"{cvx_inwallet}"+Style.RESET_ALL, end=' ')
        total += cvx_inwallet * myarray[-1]["USDcvx"]
    if crv3pool_inwallet > 0:
        print("t"+f"{crv3pool_inwallet}"+Style.RESET_ALL, end=' ')
        total += crv3pool_inwallet * myarray[-1]["USD3pool"]
    if fxslocked_inwallet > 0:
        print("ff"+Fore.BLUE+f"{fxslocked_inwallet}"+Style.RESET_ALL, end=' ')
        total += fxslocked_inwallet * myarray[-1]["FRAX"]
    if fxs_inwallet > 0:
        print("f"+Fore.BLUE+f"{fxs_inwallet}"+Style.RESET_ALL, end=' ')
        total += fxs_inwallet * myarray[-1]["FRAX"]

    print("] in wallet"+Style.DIM+f" (${total:5.2f})"+Style.RESET_ALL, end='  ')

if __name__ == "__main__":
    print("this module is not meant to be run solo")