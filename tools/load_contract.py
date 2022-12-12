#!/usr/bin/env python3
"""contract helper functions"""
# pylint: disable=C0103,C0116,C0301,W0105,E0401,R0914
import json
import os.path
from etherscan.contracts import Contract #py_etherscan_api

def load_contract(_contract, _eth_connect,abi_address='',lp_abi=False,minter_abi=False,stakedao_abi=False):
    # sourcery skip: move-assign
    abi_contract = _contract
    if _contract == "0x9D0464996170c6B9e75eED71c68B99dDEDf279e8":  #HACK for weird crv/cvxcrv pool proxy
        abi_contract = "0x4a4d7868390ef5cac51cda262888f34bd3025c3f"
    elif lp_abi:
        abi_contract = "0x98638FAcf9a3865cd033F36548713183f6996122"
    elif minter_abi:
        abi_contract = "0x8282BD15dcA2EA2bDf24163E8f2781B30C43A2ef" 
    elif stakedao_abi:
        abi_contract = "0x2717c6A0029d63E90eB12283507E06BF77A9754d"     
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
