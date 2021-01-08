#!/usr/bin/env python3
"""curve"""
# pylint: disable=C0103,C0301,W0105,E0401,R0914,C0411
import time
import json
import sys
import microdotphat
import rainbowhat
from rainbowhat_ledfunctions import rainbow_led_pricechange
rainbowhat.rainbow.set_clear_on_exit(False)

try:
    vala = int(sys.argv[1])
except:
    vala = 0

rainbowhat.lights.red.off()    #hack for starting led
rainbowhat.lights.green.off()    #hack for starting led
rainbowhat.lights.blue.off()    #hack for starting led

microdotphat.set_clear_on_exit(False)
microdotphat.set_rotate180(1-vala)

file_name = "ghistory.json"
oldstring = "0"

def update_led_curve():
    with open(file_name, 'r') as openfile:
        try:
            myarray = json.load(openfile)
            eoa = 0-len(myarray)
            USD = myarray[-1]["USD"]
            mystring = format(round(myarray[-1]["claim"]-myarray[eoa]["claim"], 4), '.4f')
            myfloat = round((myarray[-1]["claim"]-myarray[eoa]["claim"])*USD*24*365/myarray[-1]["invested"]*100, 2)
            #print(myarray[-1]["claim"],myarray[eoa]["claim"],eoa)
            rainbowhat.display.print_float(myfloat)
            rainbowhat.display.show()
        except:
            mystring = "0.0"
            myfloat = 0.0
            USD = 1
    return mystring, myfloat, USD

if __name__ == "__main__":
    change = -1
    historyarray = []
    USD = 0
    while True:
        newstring, newfloat, USD = update_led_curve()
        if newstring != oldstring and float(newstring) > 0:
            historyarray.append(float(newstring))
            if len(historyarray) > 10:
                del historyarray[0]
            if newstring > oldstring:
                change = change + 1
            else:
                change = change - 1
            print("\033[1D  ", change)
            change = min(max(change, -10), 10)
            rainbow_led_pricechange(change)
            oldstring = newstring

        print("\r", newstring, str(newfloat).zfill(2), round(sum(historyarray)/len(historyarray), 4), USD, historyarray, end='  ')
        microdotphat.write_string(format(round(sum(historyarray)/len(historyarray), 4), '.4f'), offset_x=0, kerning=False)
        microdotphat.show()
        for z in '▁▂▃▄▅▆▇█▇▆▅▄▃▁ ':
            print('\b' + z, end='', flush=True)
            time.sleep(.5)
