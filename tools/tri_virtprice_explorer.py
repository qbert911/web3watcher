#!/usr/bin/env python3
"""curve"""
# pylint: disable=C0103,C0116,C0301,W0105,E0401,R0914

import json
file_nameh = "../history/history_archive.json"
def tri_value():
    lastb = lasta = 1
    with open(file_nameh, 'r') as openfile:
        myarrayh = json.load(openfile)
    for x in range(0, len(myarrayh)):
        try:
            a = myarrayh[x]["Rvirtprice"]
            b = myarrayh[x]["Nvirtprice"]
            trix_value = myarrayh[-1]["trix_rewards"][2]/myarrayh[-1]["trix_rewards"][1]

            cvx_value = myarrayh[-1]["cvx_rewards"][2]/myarrayh[-1]["cvx_rewards"][1]
            print(myarrayh[x]["human_time"],round((a-lasta)*10000000,2),round((b-lastb)*10000000,2),trix_value,cvx_value)
            lastb = b
            lasta = a
        except:
            pass

if __name__ == "__main__":
    tri_value()
