#!/usr/bin/env python3
"""curve"""
# pylint: disable=C0103,C0116,C0301,W0105,E0401,R0914
import time
import json
from pycoingecko import CoinGeckoAPI
cg = CoinGeckoAPI()

import http.client
conn = http.client.HTTPSConnection("coingecko.p.rapidapi.com")
headers = {
    'x-rapidapi-key': "7227f72d90msh73467548a52502dp1930eajsn3980c4e35eee",
    'x-rapidapi-host': "coingecko.p.rapidapi.com"
    }

def update_price(coin_type, print_symbola='', print_symbolb='',fallback=-1):
    USD = -1
    while USD == -1:
        try:
            print(print_symbola+("\b"*len(print_symbola)), end='', flush=True)
            USD = cg.get_price(ids=coin_type, vs_currencies='usd')[coin_type]["usd"]       
            #time.sleep(1)
            print(print_symbolb, end='', flush=True)
        except Exception:
            print("Z", end='', flush=True)
            #time.sleep(10)
            return fallback
    return USD

def update_price2(coin_type, print_symbola='', print_symbolb='',fallback=-1):
    USD = -1
    while USD == -1:
        try:
            print(print_symbola+("\b"*len(print_symbola)), end='', flush=True)
            conn.request("GET", "/simple/price?ids="+coin_type+"&vs_currencies=usd", headers=headers)
            jsonl = json.loads(conn.getresponse().read())
            #print(jsonl)
            USD = jsonl[coin_type]["usd"]
            #time.sleep(5)
            print(print_symbolb, end='', flush=True)
        except Exception:
            print("Z", end='', flush=True)
            #time.sleep(10)
            return fallback
    return USD

if __name__ == "__main__":
    print(update_price("clever-cvx",'▸','▹',0))
    print(update_price("conic-finance",'▹','▸',0))