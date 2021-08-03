#!/usr/bin/env python3
import json
import urllib.request
with urllib.request.urlopen("https://api.curve.fi/api/getApys") as url:
    thisarray = json.loads(url.read().decode())

mytable = []
for key, value in thisarray["data"].items():
    if key != "generatedTimeMs":
        try:
            mytup = key, float(value["baseApy"]), value["crvApy"]*2.5, float(value["baseApy"])+(value["crvApy"]*2.5)
            mytable.append(mytup)
        except:
            print("key error")

stable = sorted(mytable, key=lambda a: a[3])
for x in range(1, len(stable)):
    print(stable[x][0].rjust(10),str(format(round(stable[x][3],2),'5.2f')).rjust(5),end=" ")
    print("=",str(format(stable[x][2],'5.2f')).rjust(5),"+",str(format(stable[x][1],'4.2f')).rjust(4))
