#!/usr/bin/env python3
"""curve"""
# pylint: disable=C0103,C0116,C0301,W0105,E0401,R0914
import json
file_nameh = "../history/history_archive.json"
with open(file_nameh, 'r') as openfile:
    myarrayh = json.load(openfile)

def virtprice_inspector():
    lastb = lasta = 1
    for x in range(0, len(myarrayh)):
        try:
            a = myarrayh[x]["Rvirtprice"]
            b = myarrayh[x]["Nvirtprice"]
            print(myarrayh[x]["human_time"],str(round((a-lasta)*10_000_000)).rjust(5),str(round((b-lastb)*10_000_000)).rjust(5))
            lastb = b
            lasta = a
        except Exception:
            pass

if __name__ == "__main__":
    virtprice_inspector()
