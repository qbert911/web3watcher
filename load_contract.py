#!/usr/bin/env python3
"""tripool functions"""
# pylint: disable=C0103,C0116,C0301,W0105,E0401,R0914
import json
import os.path
from etherscan.contracts import Contract

def load_contract(_contract, _eth_connect):
    key = 'WXPQDYFIT982E3GPJR9JEHXHNYRADB34BN'
    address = _contract
    file_name = 'abi/'+_contract+'.json'
    if not os.path.isfile(file_name):
        api = Contract(address=address, api_key=key)
        _this_abi = api.get_abi()
        print("Downloading missing abi for ", _contract)
        json.dump(_this_abi, open(file_name, "w"), indent=4)          #Output dictionary to minute file
    else:
        _this_abi = json.load(open(file_name, 'r'))

    return _eth_connect.eth.contract(_contract, abi=_this_abi).functions

def call_me(function):
    """input filtering"""
    x = function.call()
    if isinstance(x, list):
        x = x[0]
    if 0 < x < 10000:
        print("\n odd output when calling "+str(function),x)
    return x
