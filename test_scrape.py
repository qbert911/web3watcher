#!/usr/bin/env python3
import urllib.request

try:
    webpage=str(urllib.request.urlopen("http://192.168.0.198:4333/https://www.hotbit.io/invest/detail/776").read())
    try:
        mypos=webpage.index('%        ')
        crv_interest_hotbit = webpage[mypos-5:mypos]
    except:
        crv_interest_hotbit = "yy.yy"
except:
    crv_interest_hotbit = "xx.xx"

print(webpage)
print(mypos)
print("crv_hotbit_interest:",crv_interest_hotbit)
