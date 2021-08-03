#!/usr/bin/env python3
"""curve"""
# pylint: disable=C0103,C0116,C0301,W0105,E0401,R0914
import json

maxhistlen = 170

def sweep_history_log():
    file_nameh = "../ghistoryh.json"
    file_nameha = "../history/history_archive.json"

    with open(file_nameh, 'r') as openfile:
        myarrayh = json.load(openfile)

    with open(file_nameha, 'r') as openfile:
        myarrayha = json.load(openfile)

    sync = 0
    print("\nBefore\nArchive:", len(myarrayha),myarrayha[0]["human_time"], myarrayha[-1]["human_time"])
    print("Cur log:", len(myarrayh),myarrayh[0]["human_time"], myarrayh[-1]["human_time"])
    for x in range(len(myarrayh)):
        if sync == 1:
            myarrayha.append(myarrayh[x])
        if myarrayh[x]["human_time"] == myarrayha[-1]["human_time"] and sync != 1:
            print("\nsync at",x,myarrayh[x]["human_time"])
            sync = 1

    while len(myarrayh) > maxhistlen:
        del myarrayh[0]

    json.dump(myarrayha, open(file_nameha, "w"), indent=4)
    json.dump(myarrayh, open(file_nameh, "w"), indent=4)
    print("\nAfter\nArchive:", len(myarrayha),myarrayha[0]["human_time"], myarrayha[-1]["human_time"])
    print("Cur log:", len(myarrayh),myarrayh[0]["human_time"], myarrayh[-1]["human_time"],"\n")

if __name__ == "__main__":
    sweep_history_log()
