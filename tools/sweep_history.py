#!/usr/bin/env python3
"""curve"""
# pylint: disable=C0103,C0116,C0301,W0105,E0401,R0914
import json

maxhistlen = 350

def sweep_history_log():
    file_nameh = "ghistoryh.json"
    file_nameha = "history/history_archive.json"

    with open(file_nameh, 'r') as openfile:
        myarrayh = json.load(openfile)

    with open(file_nameha, 'r') as openfile:
        myarrayha = json.load(openfile)

    archive_length =  len(myarrayha)
    sync = 0
    print("\nBefore\nArchive:", archive_length, myarrayha[0]["human_time"], myarrayha[-1]["human_time"])
    print("Cur log:", len(myarrayh), myarrayh[0]["human_time"], myarrayh[-1]["human_time"])
    for x in range(len(myarrayh)):
        if sync == 1:
            myarrayha.append(myarrayh[x])
        elif myarrayh[x]["human_time"] == myarrayha[-1]["human_time"]:
            sync = 1

    if sync == 0:
        for x in range(len(myarrayh)):
            myarrayha.append(myarrayh[x])
        print("\nno sync found, so adding all records")

    while len(myarrayh) > maxhistlen:
        del myarrayh[0]

    print("\nAfter\nCur log:", len(myarrayh), myarrayh[0]["human_time"], myarrayh[-1]["human_time"])
    json.dump(myarrayh, open(file_nameh, "w"), indent=4)
    print("Archive:", len(myarrayha), myarrayha[0]["human_time"], myarrayha[-1]["human_time"])
    print("\nsync at", x+1)
    print("added",len(myarrayha)-archive_length,end='\n\n')

    if archive_length <  len(myarrayha):
        json.dump(myarrayha, open(file_nameha, "w"), indent=4)
if __name__ == "__main__":
    sweep_history_log()
