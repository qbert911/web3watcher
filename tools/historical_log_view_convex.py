#!/usr/bin/env python3
"""curve"""
# pylint: disable=C0103,C0116,C0301,W0105,E0401,R0914
import sys, json, csv
from colorama import Fore, Style
import sweep_history

def show_me(inputs, inpute, myarrayh,flag_tripped = 0):
 
    try:
        diffcvx = max(0,myarrayh[inputs]["cvxeth_rewards"][2]-myarrayh[inpute]["cvxeth_rewards"][2]) +\
                max(0,myarrayh[inputs]["cvxeth_rewards"][3][0]['amount']-myarrayh[inpute]["cvxeth_rewards"][3][0]['amount'])+\
                max(0,myarrayh[inputs]["crvsquared_rewards"][2]-myarrayh[inpute]["crvsquared_rewards"][2]) +\
                max(0,myarrayh[inputs]["crvsquared_rewards"][3][0]['amount']-myarrayh[inpute]["crvsquared_rewards"][3][0]['amount'])+\
                max(0,myarrayh[inputs]["spelleth_rewards"][2]-myarrayh[inpute]["spelleth_rewards"][2]) +\
                max(0,myarrayh[inputs]["fxslocked_rewards"][2]-myarrayh[inpute]["fxslocked_rewards"][2]) +\
                max(0,myarrayh[inputs]["crvstaked_rewards"][2]-myarrayh[inpute]["crvstaked_rewards"][2])+\
                max(0,myarrayh[inputs]["fxslocked_rewards"][3][0]['amount']-myarrayh[inpute]["fxslocked_rewards"][3][0]['amount'])+\
                max(0,(myarrayh[inputs]["fxslocked_rewards"][3][1]['amount']-myarrayh[inpute]["fxslocked_rewards"][3][1]['amount'])*myarrayh[inputs]["FRAX"]/myarrayh[inputs]["USDcvx"])   
    except:
        try:
            diffcvx = max(0,myarrayh[inputs]["cvxeth_rewards"][2]-myarrayh[inpute]["cvxeth_rewards"][2]) +\
                    max(0,myarrayh[inputs]["cvxeth_extracvx"]-myarrayh[inpute]["cvxeth_extracvx"])+\
                    max(0,myarrayh[inputs]["crvsquared_rewards"][2]-myarrayh[inpute]["crvsquared_rewards"][2]) +\
                    max(0,myarrayh[inputs]["crvsquared_extracvx"]-myarrayh[inpute]["crvsquared_extracvx"])+\
                    max(0,myarrayh[inputs]["spelleth_rewards"][2]-myarrayh[inpute]["spelleth_rewards"][2]) +\
                    max(0,myarrayh[inputs]["fxslocked_rewards"][2]-myarrayh[inpute]["fxslocked_rewards"][2]) +\
                    max(0,myarrayh[inputs]["crvstaked_rewards"][2]-myarrayh[inpute]["crvstaked_rewards"][2])+\
                    max(0,myarrayh[inputs]["fxslocked_extracvx"]-myarrayh[inpute]["fxslocked_extracvx"])+\
                    max(0,(myarrayh[inputs]["fxslocked_extrafxs"]-myarrayh[inpute]["fxslocked_extrafxs"])*myarrayh[inputs]["FRAX"]/myarrayh[inputs]["USDcvx"])   
        except:
            diffcvx = 0

    try:
        diffcrv = max(0,(myarrayh[inputs]["claim"]-myarrayh[inpute]["claim"])) +\
                max(0,((myarrayh[inputs]["cvxlocked_rewards"][1]-myarrayh[inpute]["cvxlocked_rewards"][1])*myarrayh[inputs]["USDcvxCRV"]/myarrayh[inputs]["USD"])) +\
                max(0,myarrayh[inputs]["crvsquared_rewards"][1]-myarrayh[inpute]["crvsquared_rewards"][1]) +\
                max(0,myarrayh[inputs]["cvxeth_rewards"][1]-myarrayh[inpute]["cvxeth_rewards"][1]) +\
                max(0,myarrayh[inputs]["spelleth_rewards"][1]-myarrayh[inpute]["spelleth_rewards"][1]) +\
                max(0,myarrayh[inputs]["fxslocked_rewards"][1]-myarrayh[inpute]["fxslocked_rewards"][1]) +\
                max(0,myarrayh[inputs]["crvstaked_rewards"][1]-myarrayh[inpute]["crvstaked_rewards"][1])   
    except:
        diffcrv = 0

    try:
        diff3pool = max(0,((myarrayh[inputs]["crvstaked_rewards"][3]-myarrayh[inpute]["crvstaked_rewards"][3])/myarrayh[inputs]["USD"]))  
    except:
        diff3pool = 0

    try:
        spelleth_daily = max(0,myarrayh[inputs]["spelleth_rewards"][1]-myarrayh[inpute]["spelleth_rewards"][1]\
                    +((myarrayh[inputs]["spelleth_rewards"][2]-myarrayh[inpute]["spelleth_rewards"][2])*myarrayh[inputs]["USDcvx"]/myarrayh[inputs]["USD"]))\
                    / (60)*60

        crvstaked_daily = max(0,myarrayh[inputs]["crvstaked_rewards"][1]-myarrayh[inpute]["crvstaked_rewards"][1]\
                    +((myarrayh[inputs]["crvstaked_rewards"][2]-myarrayh[inpute]["crvstaked_rewards"][2])*myarrayh[inputs]["USDcvx"]/myarrayh[inputs]["USD"])\
                    +((myarrayh[inputs]["crvstaked_rewards"][3]-myarrayh[inpute]["crvstaked_rewards"][3])/myarrayh[inputs]["USD"]))\
                    / (60)*60  

        cvxeth_daily = max(0,myarrayh[inputs]["cvxeth_rewards"][1]-myarrayh[inpute]["cvxeth_rewards"][1]\
                    +((myarrayh[inputs]["cvxeth_rewards"][2]-myarrayh[inpute]["cvxeth_rewards"][2])*myarrayh[inputs]["USDcvx"]/myarrayh[inputs]["USD"])\
                    +((myarrayh[inputs]["cvxeth_rewards"][3][0]['amount']-myarrayh[inpute]["cvxeth_rewards"][3][0]['amount'])*myarrayh[inputs]["USDcvx"]/myarrayh[inputs]["USD"]))\
                    / (60)*60   

        fxslocked_daily = max(0,myarrayh[inputs]["fxslocked_rewards"][1]-myarrayh[inpute]["fxslocked_rewards"][1]\
                    +((myarrayh[inputs]["fxslocked_rewards"][2]-myarrayh[inpute]["fxslocked_rewards"][2])*myarrayh[inputs]["USDcvx"]/myarrayh[inputs]["USD"])\
                    +((myarrayh[inputs]["fxslocked_rewards"][3][0]['amount']-myarrayh[inpute]["fxslocked_rewards"][3][0]['amount'])*myarrayh[inputs]["USDcvx"]/myarrayh[inputs]["USD"])\
                    +((myarrayh[inputs]["fxslocked_rewards"][3][1]['amount']-myarrayh[inpute]["fxslocked_rewards"][3][1]['amount'])*myarrayh[inputs]["FRAX"]/myarrayh[inputs]["USD"]))\
                    / (60)*60

        crvsquared_daily = max(0,myarrayh[inputs]["crvsquared_rewards"][1]-myarrayh[inpute]["crvsquared_rewards"][1]\
                    +((myarrayh[inputs]["crvsquared_rewards"][2]-myarrayh[inpute]["crvsquared_rewards"][2])*myarrayh[inputs]["USDcvx"]/myarrayh[inputs]["USD"])\
                    +((myarrayh[inputs]["crvsquared_rewards"][3][0]['amount']-myarrayh[inpute]["crvsquared_rewards"][3][0]['amount'])*myarrayh[inputs]["USDcvx"]/myarrayh[inputs]["USD"]))\
                    / (60)*60
    except Exception:
        try:
            spelleth_daily = max(0,myarrayh[inputs]["spelleth_rewards"][1]-myarrayh[inpute]["spelleth_rewards"][1]\
                        +((myarrayh[inputs]["spelleth_rewards"][2]-myarrayh[inpute]["spelleth_rewards"][2])*myarrayh[inputs]["USDcvx"]/myarrayh[inputs]["USD"]))\
                        / (60)*60

            crvstaked_daily = max(0,myarrayh[inputs]["crvstaked_rewards"][1]-myarrayh[inpute]["crvstaked_rewards"][1]\
                        +((myarrayh[inputs]["crvstaked_rewards"][2]-myarrayh[inpute]["crvstaked_rewards"][2])*myarrayh[inputs]["USDcvx"]/myarrayh[inputs]["USD"])\
                        +((myarrayh[inputs]["crvstaked_rewards"][3]-myarrayh[inpute]["crvstaked_rewards"][3])/myarrayh[inputs]["USD"]))\
                        / (60)*60  

            cvxeth_daily = max(0,myarrayh[inputs]["cvxeth_rewards"][1]-myarrayh[inpute]["cvxeth_rewards"][1]\
                        +((myarrayh[inputs]["cvxeth_rewards"][2]-myarrayh[inpute]["cvxeth_rewards"][2])*myarrayh[inputs]["USDcvx"]/myarrayh[inputs]["USD"])\
                        +((myarrayh[inputs]["cvxeth_extracvx"]-myarrayh[inpute]["cvxeth_extracvx"])*myarrayh[inputs]["USDcvx"]/myarrayh[inputs]["USD"]))\
                        / (60)*60   

            fxslocked_daily = max(0,myarrayh[inputs]["fxslocked_rewards"][1]-myarrayh[inpute]["fxslocked_rewards"][1]\
                        +((myarrayh[inputs]["fxslocked_rewards"][2]-myarrayh[inpute]["fxslocked_rewards"][2])*myarrayh[inputs]["USDcvx"]/myarrayh[inputs]["USD"])\
                        +((myarrayh[inputs]["fxslocked_extracvx"]-myarrayh[inpute]["fxslocked_extracvx"])*myarrayh[inputs]["USDcvx"]/myarrayh[inputs]["USD"])\
                        +((myarrayh[inputs]["fxslocked_extrafxs"]-myarrayh[inpute]["fxslocked_extrafxs"])*myarrayh[inputs]["FRAX"]/myarrayh[inputs]["USD"]))\
                        / (60)*60

            crvsquared_daily = max(0,myarrayh[inputs]["crvsquared_rewards"][1]-myarrayh[inpute]["crvsquared_rewards"][1]\
                        +((myarrayh[inputs]["crvsquared_rewards"][2]-myarrayh[inpute]["crvsquared_rewards"][2])*myarrayh[inputs]["USDcvx"]/myarrayh[inputs]["USD"])\
                        +((myarrayh[inputs]["crvsquared_extracvx"]-myarrayh[inpute]["crvsquared_extracvx"])*myarrayh[inputs]["USDcvx"]/myarrayh[inputs]["USD"]))\
                        / (60)*60
        except Exception:
            pass
    
    try:
        cvxeth_token_price = 2 * myarrayh[inputs]["cvxeth_virt"] * ((myarrayh[inputs]["USDcvx"] * myarrayh[inputs]["ETH"])**(1/2))
        spelleth_token_price = 2 * myarrayh[inputs]["spelleth_virt"] * ((myarrayh[inputs]["SPELL"] * myarrayh[inputs]["ETH"])**(1/2))
        fxslocked_token_price = 2 * myarrayh[inputs]["fxslocked_virt"] * ((myarrayh[inputs]["FRAX"] * (myarrayh[inputs]["FRAX"]*myarrayh[inputs]["fxslocked_oracle"]))**(1/2)) #hack
    except:
        try:
            cvxeth_token_price = 2 * myarrayh[inputs]["cvxeth_rewards"][4] * ((myarrayh[inputs]["USDcvx"] * myarrayh[inputs]["ETH"])**(1/2))
            spelleth_token_price = 2 * myarrayh[inputs]["spelleth_rewards"][4] * ((myarrayh[inputs]["SPELL"] * myarrayh[inputs]["ETH"])**(1/2))
            fxslocked_token_price = 2 * myarrayh[inputs]["fxslocked_rewards"][4] * ((myarrayh[inputs]["FRAX"] * (myarrayh[inputs]["FRAX"]*myarrayh[inputs]["fxslocked_oracle"]))**(1/2)) #hack
        except:
            pass #temphack

    try:
        daily_total = (cvxeth_daily + crvsquared_daily + crvstaked_daily + spelleth_daily + fxslocked_daily)*myarrayh[inputs]['USD']
        totalvalue = ((myarrayh[inputs]["cvxeth_rewards"][0]*cvxeth_token_price)+ \
                    (myarrayh[inputs]["spelleth_rewards"][0]*spelleth_token_price)+ \
                    (myarrayh[inputs]["fxslocked_rewards"][0]*fxslocked_token_price)+ \
                    (myarrayh[inputs]["crvstaked_rewards"][0]*myarrayh[inputs]['USD'])+\
                    (myarrayh[inputs]["crvsquared_rewards"][0]*myarrayh[inputs]['USD']))
        cvxeth_count = myarrayh[inputs]['cvxeth_rewards'][0]
    except:
        cvxeth_count = daily_total = totalvalue = 0.00000000000000000001

    try:
        acrv_coefficient = myarrayh[inputs]["acrv_totalunderlying"]/myarrayh[inputs]["acrv_totalsupply"]
    except:
        try:
           acrv_coefficient = myarrayh[inputs]["concentrator_virt"]
        except:
            acrv_coefficient = 1.14
    
    try:
        ctr_unclaimed_current = (211 / myarrayh[inputs]["concentrator_cvxeth_rewards"][0] *(myarrayh[inputs]["concentrator_cvxeth_rewards"][1]\
                    +(myarrayh[inputs]["concentrator_cvxeth_rewards"][2]*myarrayh[inputs]["USDcvx"]/myarrayh[inputs]["USD"])\
                    +(myarrayh[inputs]["concentrator_cvxeth_rewards"][3][0]['amount']*myarrayh[inputs]["USDcvx"]/myarrayh[inputs]["USD"])))
        ctr_unclaimed_past = (211 / myarrayh[inpute]["concentrator_cvxeth_rewards"][0] *(myarrayh[inpute]["concentrator_cvxeth_rewards"][1]\
                    +(myarrayh[inpute]["concentrator_cvxeth_rewards"][2]*myarrayh[inputs]["USDcvx"]/myarrayh[inputs]["USD"])\
                    +(myarrayh[inpute]["concentrator_cvxeth_rewards"][3][0]['amount']*myarrayh[inputs]["USDcvx"]/myarrayh[inputs]["USD"])))
    except:
        try:
            ctr_unclaimed_current = (211 / myarrayh[inputs]["concentrator_cvxeth_rewards"][0] *(myarrayh[inputs]["concentrator_cvxeth_rewards"][1]\
                        +(myarrayh[inputs]["concentrator_cvxeth_rewards"][2]*myarrayh[inputs]["USDcvx"]/myarrayh[inputs]["USD"])\
                        +(myarrayh[inputs]["concentrator_cvxeth_extracvx"]*myarrayh[inputs]["USDcvx"]/myarrayh[inputs]["USD"])))
            ctr_unclaimed_past = (211 / myarrayh[inpute]["concentrator_cvxeth_rewards"][0] *(myarrayh[inpute]["concentrator_cvxeth_rewards"][1]\
                        +(myarrayh[inpute]["concentrator_cvxeth_rewards"][2]*myarrayh[inputs]["USDcvx"]/myarrayh[inputs]["USD"])\
                        +(myarrayh[inpute]["concentrator_cvxeth_extracvx"]*myarrayh[inputs]["USDcvx"]/myarrayh[inputs]["USD"])))
        except:
            pass
        
    try:        
        concentrator_daily_crv = max(-1,ctr_unclaimed_current-ctr_unclaimed_past\
                    +((myarrayh[inputs]['concentrator_rewards_CTR']-myarrayh[inpute]['concentrator_rewards_CTR'])*acrv_coefficient*myarrayh[inputs]["USDcvxCRV"]/myarrayh[inputs]["USD"]))

        daily_total = ((concentrator_daily_crv) + cvxeth_daily + crvsquared_daily + crvstaked_daily + spelleth_daily + fxslocked_daily)*myarrayh[inputs]['USD']
        crvsquared_token_price = myarrayh[inputs]["crvsquared_rewards"][4] * ((myarrayh[inputs]["USDcvxCRV"]*.75)+(myarrayh[inputs]["USD"]*.25))
        totalvalue =((myarrayh[inputs]["cvxeth_rewards"][0]+211)*cvxeth_token_price)+ \
                    (myarrayh[inputs]["spelleth_rewards"][0]*spelleth_token_price)+ \
                    (myarrayh[inputs]["fxslocked_rewards"][0]*fxslocked_token_price)+ \
                    (myarrayh[inputs]["crvstaked_rewards"][0]*myarrayh[inputs]['USDcvxCRV'])+\
                    (myarrayh[inputs]["crvsquared_rewards"][0]*crvsquared_token_price)+\
                    (myarrayh[inputs]["cvxlocked_rewards"][0]*myarrayh[inputs]['USDcvx'])

        cvxeth_count = myarrayh[inputs]['cvxeth_rewards'][0]+211
        diffctr = concentrator_daily_crv/myarrayh[inputs]["concentrator_virt"]*myarrayh[inputs]["USD"]/myarrayh[inputs]["USDcvxCRV"]                

    except:
        ctr_unclaimed_current = ctr_unclaimed_past = ""
        concentrator_daily_crv = diffctr = 0

    mainpercentdisplay = daily_total *365/totalvalue *100

    hours_elapsed = (myarrayh[inputs]["raw_time"] - myarrayh[inpute]["raw_time"]) / (60*60) #hours elapsed
    requirements_met = diffcrv > 4 and diffcvx > .5 and cvxeth_count > 30 and round(hours_elapsed/24, 2) == 1 and diffctr >= 0
    if requirements_met or flag_tripped:
        if (len(sys.argv) -1) or requirements_met:    
            print("\rBetween", myarrayh[inpute]["human_time"], "and", myarrayh[inputs]["human_time"], end=' - ')
            print(str(round(hours_elapsed/24,2)).rjust(4), "days", end='')
            dbuffer=Fore.RED+"t"+Fore.WHITE+format((round(diff3pool, 2)), '.0f').rjust(2)
            dbuffer+=Fore.RED+"v"+Fore.WHITE+format((round(diffcrv, 2)), '.0f').rjust(2)
            dbuffer+=Fore.RED+"a"+Fore.WHITE+format((round(diffctr, 2)), '.2f').rjust(5)
            dbuffer+=Fore.RED+"x"+Fore.WHITE+format((round(diffcvx, 2)), '.2f').rjust(4)
            if requirements_met:
                undim_flag = Style.RESET_ALL
            else:
                undim_flag = ""

            print(Style.DIM+" - {"+dbuffer+"}"+undim_flag, f"  {totalvalue:7,.0f}  {cvxeth_count:3.0f}  ${daily_total:3.0f}  {mainpercentdisplay:4.1f}%"+Style.RESET_ALL,end=" ")
            difference =  min(round(mainpercentdisplay - daily_total),0)
            minim= round(min(mainpercentdisplay ,daily_total))
            sym = '█'

            if difference > 0:
                styl = Style.DIM+Fore.RED
            else:
                styl = Style.DIM+Fore.GREEN
            print(Style.DIM+Fore.YELLOW,(sym*minim)+styl+(sym*abs(int(difference))),Style.RESET_ALL)
        if not requirements_met:
            print("skipped",end="",flush=True)
        list_out = [diff3pool,diffcrv,concentrator_daily_crv,diffcvx,totalvalue,cvxeth_count,daily_total,mainpercentdisplay]

        return requirements_met, list_out
    return False, []

def daily_log():
    file_nameha = "history/history_archive.json"

    with open(file_nameha, 'r') as openfile:
        myarrayha = json.load(openfile)

    with open('historical_log_view.csv', 'w', encoding='UTF8', newline='') as f:
        flag_tripped = 0 
        for x in range(0, int((len(myarrayha)-1)/24)):
            flag_tripped, list_out = show_me((x*24)+24, (x*24), myarrayha, flag_tripped)
            if flag_tripped:
                #print(list_out)
                csv.writer(f).writerow(list_out)
        print((((len(myarrayha)-1)/24) - int((len(myarrayha)-1)/24))*24)
if __name__ == "__main__":
    sweep_history.sweep_history_log()
    daily_log()