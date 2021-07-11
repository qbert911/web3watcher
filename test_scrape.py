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


def update_hbcrv_interest():
    if not args.Local:
        try:
            webpage1=urllib.request.urlopen("http://192.168.0.198:4333/https://www.hotbit.io/invest/detail/776")
            time.sleep(6)
            webpage = str(webpage1.read())
            try:
                mypos=webpage.index('%        ')    #webpage.index('T+1  ',200)
                hbcrv_interest = str(format(float(webpage[mypos-5:mypos]), '4.1f')).rjust(4)  #float(webpage[mypos-31:mypos-26])
            except:
                hbcrv_interest = "xx.x"
        except:
            hbcrv_interest = "ww.w"
    else:
        hbcrv_interest = "--.-"
    return hbcrv_interest
