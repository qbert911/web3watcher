#!/usr/bin/env python3
"""tripool functions"""
import time
import sys, os
from brownie import *
import tripool_calc
from datetime import datetime
import convex_examiner

def load_contract(c):
    if c == ZERO_ADDRESS:
        return None
    try:
        return Contract(c)
    except Exception:
        try:
            return Contract.from_explorer(c)
        except Exception:
            print(c,"NOT LOADED")

def main():
    gauge_bal = -1
    whale = '0x8D82Fef0d77d79e5231AE7BFcFeBA2bAcF127E2B'
    while True:
        #sys.stdout = open(os.devnull, "w")
        try:
            network.connect('mainnet-fork') #noisy
            if gauge_bal < 1:
                tri = load_contract('0x80466c64868e1ab14a1ddf27a676c3fcbe638fe5')
                tri_gauge = load_contract("0x6955a55416a06839309018A8B0cB72c4DDC11f15")
                _token = load_contract("0xdAC17F958D2ee523a2206206994597C13D831ec7")
                gauge_bal = tri_gauge.balanceOf(whale)
                print(f"Gauge balance {gauge_bal / 10 ** 18}")
            try:
                tri_gauge.withdraw(gauge_bal, True, {'from': whale}) #noisy
            except Exception:
                pass
            try:
                tri.remove_liquidity_one_coin(gauge_bal, 0, 0, {'from': whale}) #noisy
            except Exception:
                pass
            try:
                _coins = _token.balanceOf(whale) / 10 ** 6
            except Exception:
                pass
            try:
                network.disconnect() #noisy
            except Exception:
                pass

            _coins_in_covex_guage = 25  #HACK  convex_examiner.trix_getvalue(False,None)[0]
            _coins = (_coins/(gauge_bal / 10 ** 18))*((gauge_bal / 10 ** 18)+_coins_in_covex_guage)
            _sim_total = tripool_calc.tri_calc(True, gauge_bal+(_coins_in_covex_guage*(10**18))) #noisy
            sys.stdout = sys.__stdout__
            print(f"  ${_coins:,.0f}  ${_sim_total:,.0f}",datetime.now().strftime('%Y-%m-%d %H:%M:%S'),flush=True,end="")
            time.sleep(60*5)
        except Exception:
            sys.stdout = sys.__stdout__
            print("couldnt connect",datetime.now().strftime('%Y-%m-%d %H:%M:%S'),flush=True)
            try:
                network.disconnect() #noisy
            except Exception:
                pass
            print("")
            time.sleep(5)

if __name__ == "__main__":
    main()
