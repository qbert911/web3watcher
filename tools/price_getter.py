#!/usr/bin/env python3
"""curve"""
# pylint: disable=C0103,C0116,C0301,W0105,E0401,R0914
import time
from pycoingecko import CoinGeckoAPI
cg = CoinGeckoAPI()

def update_price(coin_type, print_symbola='', print_symbolb='',fallback=-1):
    USD = -1
    while USD == -1:
        try:
            print(print_symbola+("\b"*len(print_symbola)), end='', flush=True)
            USD = cg.get_price(ids=coin_type, vs_currencies='usd')[coin_type]["usd"]       
            print(print_symbolb, end='', flush=True)
            time.sleep(1)
        except Exception:
            print("Z", end='', flush=True)
            #time.sleep(10)
            return fallback
    return USD
