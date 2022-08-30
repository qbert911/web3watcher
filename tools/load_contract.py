#!/usr/bin/env python3
"""contract helper functions"""
# pylint: disable=C0103,C0116,C0301,W0105,E0401,R0914
import json
import os.path
from etherscan.contracts import Contract #py_etherscan_api

def load_contract(_contract, _eth_connect,abi_address=""):
    # sourcery skip: move-assign
    abi_contract = _contract
    if str(abi_address) != "":
        abi_contract = abi_address

    key = 'WXPQDYFIT982E3GPJR9JEHXHNYRADB34BN'   #HACK My etherscan api key
    file_name = f'abi/{_contract}.json'
    if not os.path.isfile(file_name):
        api = Contract(address=abi_contract, api_key=key)
        try:
            _this_abi = api.get_abi()
            print("Downloading missing abi for", _contract)
            json.dump(_this_abi, open(file_name, "w"), indent=4)
        except Exception:
            print("unable to download missing abi for", _contract)
    else:
        _this_abi = json.load(open(file_name, 'r'))

    return _eth_connect.eth.contract(_contract, abi=_this_abi).functions

def call_me(function,expecting_list=False):
    """input filtering"""
    x = function.call()
    if isinstance(x, list):
        if not expecting_list:
            print("\n unexpected list found when calling: ",function,x)
        x = x[0]
    if 0 < x < 10000:
        print("\n odd output when calling "+str(function),x)
    return x
