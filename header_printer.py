import time
from colorama import Fore, Style
from tools.load_contract import load_contract
import status_line_printer

MY_WALLET_ADDRESS = "0x8D82Fef0d77d79e5231AE7BFcFeBA2bAcF127E2B"

#color dictionary
cd = { 
        "eth": f"{Fore.CYAN}{Style.DIM}",
        "usd": f"{Fore.GREEN}{Style.DIM}",
        "acrv": f"{Fore.YELLOW}{Style.DIM}"
     }

def concentrator_header_display(myarray,myarrayh,lookback):
    #duplicate code begin
    eoa = 0 - len(myarray)
    extramins = round((myarray[-1]["raw_time"]-myarray[eoa]["raw_time"])/60)+eoa
    month, day, hour, minut = map(str, time.strftime("%m %d %H %M").split())
    #duplicate code end

    ctreth_token_price = 2 * ((myarray[-1]["CTR"] * myarray[-1]["ETH"])**(1/2))
    ctr_ctr_owned = ctreth_token_price / 2 / myarray[-1]["CTR"] *myarray[-1]['ctreth_balance']
    ctr_eth_owned = ctreth_token_price / 2 / myarray[-1]["ETH"] *myarray[-1]['ctreth_balance']

    print("ctR/Eth CONC", f"  {Style.DIM}{ctreth_token_price*myarray[-1]['ctreth_balance']:5.0f}{Style.RESET_ALL}", end=" ")
    print(" "*9,f"r{ ctr_ctr_owned:4.0f} e{cd['eth']}{ctr_eth_owned:5.2f}{Style.RESET_ALL}",end='')
    print(" "*1,f"${cd['usd']}{myarray[-1]['ctreth_rewards']*myarray[-1]['concentrator_virt']* myarray[-1]['USDcvxCRV']:7.2f}{Style.RESET_ALL}", end=" ")
    #status_line_printer.show_abra(myarray, eoa, extramins, False)
    print(" "*36,f"a{cd['acrv']}{myarray[-1]['ctreth_rewards']:5.0f}{Style.RESET_ALL}",end=' ')

    label = 'cR2E'
    reward_amount = 'ctreth_rewards'
    reward_token_value = myarray[-1]['concentrator_virt']* myarray[-1]['USDcvxCRV']
    pricipal_amount = 'ctreth_balance'
    principal_token_value = ctreth_token_price
    yearly_profit_lasthour=max(0,float(myarray[-1][reward_amount])-float(myarray[eoa][reward_amount]))*reward_token_value*60*24*365/(60+extramins)
    yearly_profit_lastday=max(0,float(myarray[-1][reward_amount])-float(myarrayh[-lookback-1][reward_amount]))*reward_token_value*24*365/(lookback+float(int(minut)/60))
    principal_value = (myarray[eoa][pricipal_amount]*principal_token_value)
    print(f"{Fore.RED}{Style.BRIGHT}{label}{Style.RESET_ALL}{yearly_profit_lasthour/principal_value*100:6.2f}% ${yearly_profit_lasthour:7.2f} | {yearly_profit_lastday/principal_value*100:6.2f}%  ${yearly_profit_lastday:7.2f}")
   
    cvxeth_token_price = 2 * myarray[-1]["cvxeth_rewards"][4] * ((myarray[-1]["USDcvx"] * myarray[-1]["ETH"])**(1/2))
    cvx_cvx_owned = 211 * myarray[-1]["concentrator_x2e_virt"] * cvxeth_token_price / 2 / myarray[-1]["USDcvx"]
    cvx_eth_owned = 211 * myarray[-1]["concentrator_x2e_virt"] * cvxeth_token_price / 2 / myarray[-1]["ETH"]
    cvxeth_value = myarray[-1]['concentrator_rewards_CTR']*myarray[-1]["concentrator_virt"]* myarray[-1]['USDcvxCRV']

    print("cvX/Eth CONC", " " * 0, f"{Style.DIM}{211 * myarray[-1]['concentrator_x2e_virt'] * cvxeth_token_price:6.0f}{Style.RESET_ALL}", end=" ")
    print(" "*9,f"x{cvx_cvx_owned:4.0f} e{cvx_eth_owned:5.2f}",end='')
    print(" "*1,f"${cd['usd']}{cvxeth_value:7.2f}{Style.RESET_ALL}",end=" ")
    concentrator_hourly, ctr_unclaimed_current, diffctr, ctr_unclaimed_tvirt = status_line_printer.calc_concentrator_hourly(myarray,eoa,extramins,myarrayh,lookback)
    print(f"{concentrator_hourly*24*myarray[-1]['USD'] *365/(211* myarray[-1]['concentrator_x2e_virt'] *cvxeth_token_price)*100:2.0f}%",end='')
    print(" "*33,f"a{cd['acrv']}{myarray[-1]['concentrator_rewards_CTR']:5.0f}{Style.RESET_ALL}",end=" ")

    label = 'cX2E'
    reward_amount = 'concentrator_rewards_CTR'
    reward_token_value = myarray[-1]['concentrator_virt']* myarray[-1]['USDcvxCRV']
    pricipal_amount = 211 * myarray[-1]['concentrator_x2e_virt'] 
    principal_token_value = cvxeth_token_price
    yearly_profit_lasthour=max(0,float(myarray[-1][reward_amount])-float(myarray[eoa][reward_amount]))*reward_token_value*60*24*365/(60+extramins)
    yearly_profit_lastday=max(0,float(myarray[-1][reward_amount])-float(myarrayh[-lookback-1][reward_amount]))*reward_token_value*24*365/(lookback+float(int(minut)/60))
    principal_value = (pricipal_amount*principal_token_value)
    print(f"{Fore.RED}{Style.BRIGHT}{label}{Style.RESET_ALL}{yearly_profit_lasthour/principal_value*100:6.2f}% ${yearly_profit_lasthour:7.2f} | {yearly_profit_lastday/principal_value*100:6.2f}%  ${yearly_profit_lastday:7.2f}")
   

def concentrator_locked_header_display(myarray,myarrayh,lookback):
    #duplicate code begin
    eoa = 0 - len(myarray)
    extramins = round((myarray[-1]["raw_time"]-myarray[eoa]["raw_time"])/60)+eoa
    month, day, hour, minut = map(str, time.strftime("%m %d %H %M").split())
    #duplicate code end    
    
    print("Locked CTR", " " * 8, f"{Style.DIM}{Style.RESET_ALL}", end=" ") #{myarray[-1]['concentrator_ve_locked']*myarray[-1]['CTR']:6.0f}
    print(" "*9,f"r{myarray[-1]['concentrator_ve_locked']:4.0f}{Style.DIM} ({myarray[-1]['concentrator_ve_current']:4.0f}){Style.RESET_ALL}", end='')
    print(" "*1,f"${cd['usd']}{myarray[-1]['concentrator_ve_claimable']*myarray[-1]['concentrator_virt']* myarray[-1]['USDcvxCRV']:7.2f}{Style.RESET_ALL}",end ='')
    print(" "*37,f"a{cd['acrv']}{myarray[-1]['concentrator_ve_claimable']:5.0f}{Style.RESET_ALL}",end= ' ')
    
    label = 'vCTR'
    reward_amount = 'concentrator_ve_claimable'
    reward_token_value = myarray[-1]['concentrator_virt']* myarray[-1]['USDcvxCRV']
    pricipal_amount = 'concentrator_ve_current'
    principal_token_value = myarray[-1]['CTR']
    yearly_profit_lasthour=max(0,float(myarray[-1][reward_amount])-float(myarray[eoa][reward_amount]))*reward_token_value*60*24*365/(60+extramins)
    yearly_profit_lastday=max(0,float(myarray[-1][reward_amount])-float(myarrayh[-lookback-1][reward_amount]))*reward_token_value*24*365/(lookback+float(int(minut)/60))
    principal_value = (myarray[eoa][pricipal_amount]*principal_token_value)
    print(f"{Fore.RED}{Style.BRIGHT}{label}{Style.RESET_ALL}{yearly_profit_lasthour/principal_value*100:6.2f}% ${yearly_profit_lasthour:7.2f} | {yearly_profit_lastday/principal_value*100:6.2f}%  ${yearly_profit_lastday:7.2f}")

def clev_header_display(myarray,myarrayh,lookback):
    #HACK use cvx price * .9 for now
    print("abcCVX CLEV", " " * 1, f"{Style.DIM}{myarray[-1]['abcCVX_balance'] * myarray[-1]['USDcvx']*.9:6.0f}{Style.RESET_ALL}", end=" ")
    print(" "*8,f"xx{myarray[-1]['abcCVX_balance']:4.0f}",end=" ")
    print(" "*7,f"${myarray[-1]['abcCVX_rewards']*myarray[-1]['CLEV']:7.2f}", end=" ")
    print(f"{myarray[-1]['abcCVX_baseapy']:2.0f}%", end=' ')
    #status_line_printer.show_clev(myarray, eoa,extramins,"abcplaceholder","xFXS", 0, fxslocked_token_price,myarrayh,lookback,"", False)
    print(" "*31,f"cL{myarray[-1]['abcCVX_rewards']:5.2f}",end=' ')

    #duplicate code begin
    eoa = 0 - len(myarray)
    extramins = round((myarray[-1]["raw_time"]-myarray[eoa]["raw_time"])/60)+eoa
    month, day, hour, minut = map(str, time.strftime("%m %d %H %M").split())
    #duplicate code end

    label = 'aCVX'
    reward_amount = 'abcCVX_rewards'
    reward_token_value = myarray[-1]['CLEV']
    pricipal_amount = 'abcCVX_balance'
    principal_token_value = myarray[-1]["USDcvx"]*.9
    yearly_profit_lasthour=max(0,float(myarray[-1][reward_amount])-float(myarray[eoa][reward_amount]))*reward_token_value*60*24*365/(60+extramins)
    yearly_profit_lastday=max(0,float(myarray[-1][reward_amount])-float(myarrayh[-lookback-1][reward_amount]))*reward_token_value*24*365/(lookback+float(int(minut)/60))
    principal_value = (myarray[eoa][pricipal_amount]*principal_token_value)
    print(f"{Fore.RED}{Style.BRIGHT}{label}{Style.RESET_ALL}{yearly_profit_lasthour/principal_value*100:6.2f}% ${yearly_profit_lasthour:7.2f} | {yearly_profit_lastday/principal_value*100:6.2f}%  ${yearly_profit_lastday:7.2f}")

def conic_header_display(myarray,myarrayh,lookback):
    #duplicate code begin
    eoa = 0 - len(myarray)
    extramins = round((myarray[-1]["raw_time"]-myarray[eoa]["raw_time"])/60)+eoa
    month, day, hour, minut = map(str, time.strftime("%m %d %H %M").split())
    #duplicate code end    
    cnceth_token_price = 2 * ((myarray[-1]["CNC"] * myarray[-1]["ETH"])**(1/2))
    cnc_cnc_owned = cnceth_token_price / 2 / myarray[-1]["CNC"] *myarray[-1]['cnceth_concentrator_rewards'][0]
    cnc_eth_owned = cnceth_token_price / 2 / myarray[-1]["ETH"] *myarray[-1]['cnceth_concentrator_rewards'][0]
    
    print("cNc/Eth CONE", f"  {Style.DIM}{cnceth_token_price*myarray[-1]['cnceth_concentrator_rewards'][0]:5.0f}{Style.RESET_ALL}", end=" ")
    print(" "*9,f"N{ cnc_cnc_owned:4.0f} e{cnc_eth_owned:5.2f}",end='')
    #print(" "*1,f"${myarray[-1]['cnceth_rewards']*myarray[-1]['CNC']:7.2f}", end=" ")
    #status_line_printer.show_cone?(myarray, eoa, extramins, False)
    #print(" "*36,f"N{myarray[-1]['cnceth_rewards']:5.2f}",end=' ')

    label = 'lN2E'
    reward_amount = 'cnceth_rewards'
    reward_token_value = myarray[-1]['CNC']
    pricipal_amount = 'cnceth_concentrator_rewards'
    principal_token_value = cnceth_token_price
    yearly_profit_lasthour=max(0,float(myarray[-1][reward_amount])-float(myarray[eoa][reward_amount]))*reward_token_value*60*24*365/(60+extramins)
    yearly_profit_lastday=max(0,float(myarray[-1][reward_amount])-float(myarrayh[-lookback-1][reward_amount]))*reward_token_value*24*365/(lookback+float(int(minut)/60))
    principal_value = (myarray[-1][pricipal_amount][0]*principal_token_value)
    #print(f"{Fore.RED}{Style.BRIGHT}{label}{Style.RESET_ALL}{yearly_profit_lasthour/(principal_value+.000000001)*100:6.2f}% ${yearly_profit_lasthour:7.2f} | {yearly_profit_lastday/(principal_value+.000000001)*100:6.2f}%  ${yearly_profit_lastday:7.2f}")
    print()
    
def abracadabra_header_display(myarray,myarrayh,lookback):
    #duplicate code begin
    eoa = 0 - len(myarray)
    extramins = round((myarray[-1]["raw_time"]-myarray[eoa]["raw_time"])/60)+eoa
    month, day, hour, minut = map(str, time.strftime("%m %d %H %M").split())
    #duplicate code end    
    print("Spell/Eth ABRA", f"{Style.DIM}{(myarray[-1]['abra_spelleth'][0] * myarray[-1]['ETH'])+(myarray[-1]['abra_spelleth'][1] * myarray[-1]['SPELL']):5.0f}{Style.RESET_ALL}", end=" ")
    print(" "*8,f"Ks{myarray[-1]['abra_spelleth'][1]/1000:4.0f} e{myarray[-1]['abra_spelleth'][0]:5.2f}",end='')
    print(" "*1,f"${myarray[-1]['abra_spelleth'][2]*myarray[-1]['SPELL']:7.2f}", end=" ")
    status_line_printer.show_abra(myarray, eoa, extramins, False)
    print(" "*31,f"Ks{myarray[-1]['abra_spelleth'][2]/1000:5.0f}",end=" ")

    label = 'aS2E'
    reward_amount = 'abra_spelleth'
    reward_place = 2
    reward_token_value = myarray[-1]['SPELL']
    pricipal_amount = ''
    principal_token_value = ''
    yearly_profit_lasthour=max(0,float(myarray[-1][reward_amount][reward_place])-float(myarray[eoa][reward_amount][reward_place]))/(60+extramins)*reward_token_value*60*24*365
    yearly_profit_lastday=max(0,float(myarray[-1][reward_amount][reward_place])-float(myarrayh[-lookback-1][reward_amount][reward_place]))*reward_token_value*24*365/(lookback+float(int(minut)/60))
    principal_value = (myarray[-1]['abra_spelleth'][0] * myarray[-1]['ETH'])+(myarray[-1]['abra_spelleth'][1] * myarray[-1]['SPELL'])
    print(f"{Fore.RED}{Style.BRIGHT}{label}{Style.RESET_ALL}{yearly_profit_lasthour/principal_value*100:6.2f}% ${yearly_profit_lasthour:7.2f} | {yearly_profit_lastday/principal_value*100:6.2f}%  ${yearly_profit_lastday:7.2f}")




def stakedao_header_display(myarray,myarrayh,lookback):
    reward_a = myarray[-1]['stakedao_crvstaked'][1] * myarray[-1]['SDT']
    reward_b = myarray[-1]['stakedao_crvstaked'][2] * myarray[-1]['USD3pool']
    reward_c = myarray[-1]['stakedao_crvstaked'][3] * myarray[-1]['USD']
    stakedao_total_value = reward_a + reward_b + reward_c
    print("Staked SDcrv", " " * 1, f"{Style.DIM}{myarray[-1]['stakedao_crvstaked'][0] * myarray[-1]['USD']:5.0f}{Style.RESET_ALL}", end=" ")
    print(" "*8,f"sv{myarray[-1]['stakedao_crvstaked'][0]:4.0f}",end="")
    print(" "*8,f"${stakedao_total_value:7.2f}", end=" ")
    #status_line_printer.show_convex2_extracvx(myarray, eoa,extramins,"crvsquared_rewards","xV2V", 0, myarray[-1]['USDcvxCRV'], myarrayh,lookback,"",False,"") #Indicates no third pool and using token_value_modifyer
    print(" "*17,"v"+str(format(round(myarray[-1]["stakedao_crvstaked"][3],2), '5.2f')).rjust(5)," "*4,"t"+str(format(round(myarray[-1]["stakedao_crvstaked"][2],2), '5.2f')).rjust(5)+"sd"+str(format(round(myarray[-1]["stakedao_crvstaked"][1],2), '5.2f')).rjust(5))

def convex_header_display(myarray,myarrayh,lookback):

    cvxeth_value = ((myarray[-1]["cvxeth_rewards"][2]*myarray[-1]["USDcvx"])+
                  (myarray[-1]["cvxeth_rewards"][1]*myarray[-1]["USD"])+
                  (myarray[-1]["cvxeth_rewards"][3][0]['amount']*myarray[-1]["USDcvx"]))

    fxslocked_value = ((myarray[-1]["fxslocked_rewards"][2]*myarray[-1]["USDcvx"])+
                  (myarray[-1]["fxslocked_rewards"][1]*myarray[-1]["USD"])+
                  (myarray[-1]["fxslocked_rewards"][3][0]['amount']*myarray[-1]["USDcvx"])+
                  (myarray[-1]["fxslocked_rewards"][3][1]['amount']*myarray[-1]["FRAX"]))

    spelleth_value = ((myarray[-1]["spelleth_rewards"][2]*myarray[-1]["USDcvx"])+
                  (myarray[-1]["spelleth_rewards"][1]*myarray[-1]["USD"]))

    crvstaked_value = ((myarray[-1]["crvstaked_rewards"][3]*myarray[-1]["USD3pool"])+
                 (myarray[-1]["crvstaked_rewards"][2]*myarray[-1]["USDcvx"])+
                 (myarray[-1]["crvstaked_rewards"][1]*myarray[-1]["USD"]))

    cvxlocked_value = ((myarray[-1]["cvxlocked_rewards"][1]*myarray[-1]["USDcvxCRV"])+
                      (myarray[-1]["cvxlocked_rewards"][2]*myarray[-1]["FRAX"])) 

    crvsquared_value = ((myarray[-1]["crvsquared_rewards"][2]*myarray[-1]["USDcvx"])+
                  (myarray[-1]["crvsquared_rewards"][1]*myarray[-1]["USD"])+
                  (myarray[-1]["crvsquared_rewards"][3][0]['amount']*myarray[-1]["USDcvx"]))

    #tripool_token_price =  3 * ((myarray[-1]["BTC"] * myarray[-1]["ETH"])**(1/3))
    cvxeth_token_price = 2 * myarray[-1]["cvxeth_rewards"][4] * ((myarray[-1]["USDcvx"] * myarray[-1]["ETH"])**(1/2))
    #spelleth_token_price = 2 * myarray[-1]["spelleth_rewards"][4] * ((myarray[-1]["SPELL"] * myarray[-1]["ETH"])**(1/2))
    fxslocked_token_price = 2 * myarray[-1]["fxslocked_rewards"][4] * ((myarray[-1]["FRAX"] * (myarray[-1]["FRAX"]*myarray[-1]["fxslocked_oracle"]))**(1/2)) #hack
    crvsquared_token_price = myarray[-1]["crvsquared_rewards"][4] * ((myarray[-1]["USDcvxCRV"]*.75)+(myarray[-1]["USD"]*.25))

    cvx_cvx_owned = myarray[-1]["cvxeth_rewards"][0]*cvxeth_token_price / 2 / myarray[-1]["USDcvx"]
    cvx_eth_owned = myarray[-1]["cvxeth_rewards"][0]*cvxeth_token_price / 2 / myarray[-1]["ETH"]

    #spell_spell_owned = myarray[-1]["spelleth_rewards"][0]*spelleth_token_price / 2 / myarray[-1]["SPELL"]
    #spell_eth_owned = myarray[-1]["spelleth_rewards"][0]*spelleth_token_price / 2 / myarray[-1]["ETH"]

    #duplicate code begin
    eoa = 0 - len(myarray)
    extramins = round((myarray[-1]["raw_time"]-myarray[eoa]["raw_time"])/60)+eoa
    month, day, hour, minut = map(str, time.strftime("%m %d %H %M").split())
    #duplicate code end

    #print("xSpell/Eth", " " * 2, f"{Style.DIM}{myarray[-1]['spelleth_rewards'][0] * spelleth_token_price:6.0f}{Style.RESET_ALL}", end=" ")
    #print(" "*9,f"s{spell_spell_owned/1000:3.0f}k e{spell_eth_owned:5.2f}",end='')
    #print(" "*1,f"${spelleth_value:7.2f}",end=" ")
    #status_line_printer.show_convex2(myarray, eoa,extramins,"spelleth_rewards","xS2E", 0, spelleth_token_price,myarrayh,lookback,"", False) #Indicates no third pool and using token_value_modifyer
    #print(" "*13,f"v{myarray[-1]['spelleth_rewards'][1]:5.2f}x{myarray[-1]['spelleth_rewards'][2]:5.2f}")

    #print("cvX/Eth", " " * 5, f"{Style.DIM}{myarray[-1]['cvxeth_rewards'][0] * cvxeth_token_price:6.0f}{Style.RESET_ALL}", end=" ")
    #print(" "*9,f"x{cvx_cvx_owned:4.0f} e{cvx_eth_owned:5.2f}",end='')
    #print(" "*1,f"${cvxeth_value:7.2f}", end=" ")
    #status_line_printer.show_convex2_extracvx(myarray, eoa,extramins,"cvxeth_rewards","xX2E", 0, cvxeth_token_price, myarrayh,lookback,"", False, "") #Indicates no third pool and using token_value_modifyer
    #print(" "*13,"v"+str(format(round(myarray[-1]["cvxeth_rewards"][1],2), '5.2f')).rjust(5)+"x"+str(format(round(myarray[-1]["cvxeth_rewards"][2]+myarray[-1]["cvxeth_rewards"][3][0]['amount'],2), '5.2f')).rjust(5))

    print("aFXS CONC", " " * 3, f"{Style.DIM}{myarray[-1]['afxs_balance'] * myarray[-1]['afxs_virt'] * fxslocked_token_price:6.0f}{Style.RESET_ALL}", end=" ")
    print(" "*8,f"ff{myarray[-1]['afxs_balance']* myarray[-1]['afxs_virt']*2:4.0f}",end=" ")
    print(" "*7,f"{Style.DIM}${fxslocked_value:7.2f}", end=" ")
    status_line_printer.show_convex2_extrafxs(myarray, eoa,extramins,"fxslocked_rewards","xFXS", 0, fxslocked_token_price*1.1,myarrayh,lookback,"", False)
    print(" "*1,"v"+str(format(round(myarray[-1]['fxslocked_rewards'][1],2), '6.2f')).rjust(5)+"x"+str(format(round(myarray[-1]["fxslocked_rewards"][2]+myarray[-1]["fxslocked_rewards"][3][0]['amount'],2), '5.2f')).rjust(5)+"      f"+str(format(round(myarray[-1]["fxslocked_rewards"][3][1]['amount'],2), '5.2f')).rjust(5),f"{Style.RESET_ALL}",end=" ")

    label = 'aFXS'
    reward_amount = 'afxs_virt'
    reward_token_value = fxslocked_token_price
    pricipal_amount = myarray[-1]['afxs_balance'] 
    principal_token_value = fxslocked_token_price
    yearly_profit_lasthour=max(0,float(myarray[-1][reward_amount])-float(myarray[eoa][reward_amount]))*reward_token_value*60*24*365/(60+extramins)
    yearly_profit_lastday=max(0,float(myarray[-1][reward_amount])-float(myarrayh[-lookback-1][reward_amount]))*reward_token_value*24*365/(lookback+float(int(minut)/60))
    principal_value = (pricipal_amount*principal_token_value)
    #print(" "*10,f"{Fore.RED}{Style.BRIGHT}{label}{Style.RESET_ALL}{yearly_profit_lasthour/principal_value*100:6.2f}% ${yearly_profit_lasthour:7.2f} | {yearly_profit_lastday/principal_value*100:6.2f}%  ${yearly_profit_lastday:7.2f}")
    print()

    print("Locked CVX", " " * 3, f"{Style.DIM}{myarray[-1]['cvxlocked_rewards'][0] * myarray[-1]['USDcvx']:5.0f}{Style.RESET_ALL}", end="")
    print(" "*10,f"x{myarray[-1]['cvxlocked_rewards'][0]:4.0f}",end="")
    print(" "*8,f"${cvxlocked_value:7.2f}", end=" ")
    status_line_printer.show_cvxlocked_rewards(myarray, eoa, extramins, False)
    print(" "*0,"vv"+str(format(round(myarray[-1]["cvxlocked_rewards"][1],2), '6.2f')).rjust(5)," "*3,"      ff"+str(format(round(myarray[-1]["cvxlocked_rewards"][2],2), '5.2f')).rjust(5))
   
    print("CRV/cvxCRV", " " * 3, f"{Style.DIM}{myarray[-1]['crvsquared_rewards'][0] * crvsquared_token_price:5.0f}{Style.RESET_ALL}", end=" ")
    print(" "*7,f"vv{myarray[-1]['crvsquared_rewards'][0]:5.0f}",end="")
    print(" "*8,f"${crvsquared_value:7.2f}", end=" ")
    status_line_printer.show_convex2_extracvx(myarray, eoa,extramins,"crvsquared_rewards","xV2V", 0, crvsquared_token_price, myarrayh,lookback,"",False,"") #Indicates no third pool and using token_value_modifyer
    print(" "*1,"v"+str(format(round(myarray[-1]["crvsquared_rewards"][1],2), '6.2f')).rjust(5)+"x"+str(format(round(myarray[-1]["crvsquared_rewards"][2]+myarray[-1]["crvsquared_rewards"][3][0]['amount'],2), '5.2f')).rjust(5))

    print("Staked cvxCRV", " " * 0, f"{Style.DIM}{myarray[-1]['crvstaked_rewards'][0] * myarray[-1]['USDcvxCRV']:5.0f}{Style.RESET_ALL}", end="")
    print(" "*8,f"vv{myarray[-1]['crvstaked_rewards'][0]:5.0f}",end="")
    print(" "*8,f"${crvstaked_value:7.2f}", end=" ")
    status_line_printer.show_convex(myarray, eoa,extramins,"crvstaked_rewards","xCRV", 1, 1, False) #Indicates having an extra 3pool and not using token_value_modifyer
    print(" "*1,"v"+str(format(round(myarray[-1]["crvstaked_rewards"][1],2), '6.2f')).rjust(5)+"x"+str(format(round(myarray[-1]["crvstaked_rewards"][2],2), '5.2f')).rjust(5)+"t"+str(format(round(myarray[-1]["crvstaked_rewards"][3],2), '5.2f')).rjust(5))

def curve_header_display2(myarray, carray, w3, fullheader,myarrayh,lookback):
    """display detailed pool information"""
    tripool_token_price =  3 * ((myarray[-1]["BTC"] * myarray[-1]["ETH"])**(1/3))
    for i in range(len(carray["name"])):
        if carray["currentboost"][i] > 0 or fullheader:
            carray["totalsupply"][i] = round((load_contract(carray["gaugeaddress"][i],w3).totalSupply().call())/10**18, 2)
            carray["virtprice"][i] = round((load_contract(carray["swapaddress"][i],w3).get_virtual_price().call())/10**18, 6)
            carray["balanceof"][i] = round((load_contract(carray["gaugeaddress"][i],w3).balanceOf(MY_WALLET_ADDRESS).call())/10**18, 2)
            if len(carray["tokenaddress"][i]) > 1:
                carray["balanceof"][i] += round((load_contract(carray["tokenaddress"][i],w3).balanceOf(MY_WALLET_ADDRESS).call())/10**18, 2)

            print(carray["longname"][i].ljust(len(max(carray["longname"], key=len))), end='')
            print(" "*3,Style.DIM+str(format((carray["virtprice"][i]*carray["balanceof"][i]*tripool_token_price), '.0f')).rjust(4)+Style.RESET_ALL, end='') #HACK replaced with token price since only tripool remains: carray["token_value_modifyer"][i]
            if abs(round(myarray[-1][carray["name"][i]+"pool"]-round(carray["minted"][i]/10**18,2), 2)) > 0.05:
                print(" "*24,Style.DIM+"$"+str(format(round((myarray[-1][carray["name"][i]+"pool"]-(round(carray["minted"][i]/10**18,2)))*myarray[-1]["USD"], 2), '7.2f')).rjust(6)+Style.RESET_ALL, end=' ')
                eoa = 0 - len(myarray)
                extramins = round((myarray[-1]["raw_time"]-myarray[eoa]["raw_time"])/60)+eoa
                status_line_printer.show_curve(carray, myarray, myarrayh, eoa, extramins, lookback, False)
                print(" "*1,Style.DIM+str("v"+format(round(myarray[-1][carray["name"][i]+"pool"]-(round(carray["minted"][i]/10**18,2)), 2), '6.2f')).rjust(6)+Style.RESET_ALL, end=' ')
            
            print("") 

def combined_stats_display(myarray, carray, w3):
    vecrv_func = load_contract("0x5f3b5DfEb7B28CDbD7FAba78963EE202a494e2A2",w3)
    veCRV_mine = round((vecrv_func.balanceOf(MY_WALLET_ADDRESS).call())/10**18)
    veCRV_locked = round((vecrv_func.locked(MY_WALLET_ADDRESS).call()[0])/10**18)
   
    x_claimable = (myarray[-1]["crvstaked_rewards"][3]*myarray[-1]["USD3pool"]/myarray[-1]["USD"])+\
                  (myarray[-1]["crvstaked_rewards"][2]*myarray[-1]["USDcvx"]/myarray[-1]["USD"])+\
                  myarray[-1]["crvstaked_rewards"][1]+\
                  (myarray[-1]["spelleth_rewards"][2]*(myarray[-1]["USDcvx"]/myarray[-1]["USD"]))+\
                  myarray[-1]["spelleth_rewards"][1]+\
                  (myarray[-1]["cvxeth_rewards"][2]*(myarray[-1]["USDcvx"]/myarray[-1]["USD"]))+\
                  (myarray[-1]["cvxeth_rewards"][3][0]['amount']*(myarray[-1]["USDcvx"]/myarray[-1]["USD"]))+\
                  myarray[-1]["cvxeth_rewards"][1]+\
                  (myarray[-1]["crvsquared_rewards"][2]*(myarray[-1]["USDcvx"]/myarray[-1]["USD"]))+\
                  (myarray[-1]["crvsquared_rewards"][3][0]['amount']*(myarray[-1]["USDcvx"]/myarray[-1]["USD"]))+\
                  myarray[-1]["crvsquared_rewards"][1]+\
                  (myarray[-1]["cvxlocked_rewards"][1]*myarray[-1]["USDcvxCRV"]/myarray[-1]["USD"])+\
                  (myarray[-1]["cvxlocked_rewards"][2]*myarray[-1]["FRAX"]/myarray[-1]["USD"])

    print("veCRV                          Ç"+str(round(veCRV_locked)),Style.DIM+"("+str(veCRV_mine)+")"+Style.RESET_ALL,  end='')
    print(" "*1,("$"+str(format(round(x_claimable*myarray[-1]["USD"], 2),'7.2f'))).rjust(8),end ="")  
    print(" "*4,Style.DIM+" {"+Fore.RED+"v"+Fore.WHITE+str(round(myarray[-1]["crvstaked_rewards"][1]+myarray[-1]["spelleth_rewards"][1]+myarray[-1]["cvxeth_rewards"][1]+myarray[-1]["cvxlocked_rewards"][1]+myarray[-1]["crvsquared_rewards"][1],2)).rjust(6),end="")
    print(Fore.RED+"x"+Fore.WHITE+str(round(myarray[-1]["crvstaked_rewards"][2]+myarray[-1]["cvxeth_rewards"][2]+myarray[-1]["spelleth_rewards"][2]+myarray[-1]["crvsquared_rewards"][2] + myarray[-1]["cvxeth_rewards"][3][0]['amount'] + myarray[-1]["crvsquared_rewards"][3][0]['amount'],2)).rjust(5),end="")
    print(f"{Fore.RED}t{Fore.WHITE}{myarray[-1]['crvstaked_rewards'][3]:5.2f}",end='')
    print(Fore.RED+"f"+Fore.WHITE+str(round(myarray[-1]["cvxlocked_rewards"][2],2)).rjust(5)+"}"+Style.RESET_ALL+" to claim     ",end='')
    show_wallet(myarray,w3)

    eoa = 0 - len(myarray)
    if round((round(time.time())-myarray[eoa]["raw_time"])/60, 2)+eoa >= 0.5:
        print(Fore.RED+str(round(((round(time.time())-myarray[eoa]["raw_time"])/60)+eoa, 2))+Style.RESET_ALL+"oos", end=' ')
    if eoa > -61:
        print(Style.BRIGHT+Fore.RED+str(61+eoa)+Style.RESET_ALL+" minutes under 60.", end=' ')
    if sum(carray["invested"]) != myarray[eoa]["invested"]:
        print(Fore.RED+str(sum(carray["invested"]) - myarray[eoa]["invested"])+Style.RESET_ALL+" of New $ obs. data", end='')
    if myarray[-1]["crvstaked_rewards"][0] != myarray[eoa]["crvstaked_rewards"][0]:
        print(Fore.RED+str(myarray[-1]["crvstaked_rewards"][0] - myarray[eoa]["crvstaked_rewards"][0])+Style.RESET_ALL+" of New $ obs. data", end=' ')
    print("")

def show_wallet(myarray,w3):
    crv_func = load_contract("0xD533a949740bb3306d119CC777fa900bA034cd52",w3)
    cvx_token = load_contract("0x4e3FBD56CD56c3e72c1403e103b45Db9da5B9D2B",w3)
    cvxcrv_token = load_contract("0x62B9c7356A2Dc64a1969e19C23e4f579F9810Aa7",w3)
    crv3pool_token = load_contract("0x6c3F90f043a72FA612cbac8115EE7e52BDe6E490",w3)
    fxslocked_token = load_contract("0xFEEf77d3f69374f66429C91d732A244f074bdf74",w3)
    fxs_token = load_contract("0x3432B6A60D23Ca0dFCa7761B7ab56459D9C964D0",w3)

    CRV_inwallet = round((crv_func.balanceOf(MY_WALLET_ADDRESS).call())/10**18)
    cvx_inwallet = round((cvx_token.balanceOf(MY_WALLET_ADDRESS).call())/10**18)
    cvxcrv_inwallet = round((cvxcrv_token.balanceOf(MY_WALLET_ADDRESS).call())/10**18)
    crv3pool_inwallet = round((crv3pool_token.balanceOf(MY_WALLET_ADDRESS).call())/10**18)
    fxslocked_inwallet = round((fxslocked_token.balanceOf(MY_WALLET_ADDRESS).call())/10**18,1)
    fxs_inwallet = round((fxs_token.balanceOf(MY_WALLET_ADDRESS).call())/10**18,1)

    total = 0
    print("[", end=' ')
    if CRV_inwallet > 0:
        print(f"v{Fore.CYAN}" + f"{CRV_inwallet}" + Style.RESET_ALL, end=' ')
        total += CRV_inwallet * myarray[-1]["USD"]
    if cvxcrv_inwallet > 0:
        print(f"vv{Fore.CYAN}" + f"{cvxcrv_inwallet}" + Style.RESET_ALL, end=' ')
        total += cvxcrv_inwallet * myarray[-1]["USDcvxCRV"]
    if cvx_inwallet > 0:
        print(f"x{Fore.BLUE}" + f"{cvx_inwallet}" + Style.RESET_ALL, end=' ')
        total += cvx_inwallet * myarray[-1]["USDcvx"]
    if crv3pool_inwallet > 0:
        print(f"t{crv3pool_inwallet}{Style.RESET_ALL}", end=' ')
        total += crv3pool_inwallet * myarray[-1]["USD3pool"]
    if fxslocked_inwallet > 0:
        print(f"ff{Fore.BLUE}" + f"{fxslocked_inwallet}" + Style.RESET_ALL, end=' ')
        total += fxslocked_inwallet * myarray[-1]["FRAX"]
    if fxs_inwallet > 0:
        print(f"f{Fore.BLUE}" + f"{fxs_inwallet}" + Style.RESET_ALL, end=' ')
        total += fxs_inwallet * myarray[-1]["FRAX"]

    print(f"] in wallet{Style.DIM}" + f" (${total:5.2f})" + Style.RESET_ALL, end='  ')

if __name__ == "__main__":
    print("this module is not meant to be run solo")