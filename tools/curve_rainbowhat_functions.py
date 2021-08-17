#!/usr/bin/env python3
# pylint: disable=C0103,E0401
"""write to the seven leds on the top of the rainbow HAT"""
try:
    import smbus
    import rainbowhat
    import microdotphat
    rainbowhat.rainbow.set_clear_on_exit(False)

    bus = smbus.SMBus(1) # 1 indicates /dev/i2c-1
except:
    pass

red = [2, 0, 0]
green = [0, 2, 0]
gray = [1, 1, 1]
blank = [0, 0, 0]
brightness = .8

def rainbow_show_boost_status(array):
    """write to leds"""
    rainbowhat.rainbow.set_clear_on_exit(False)
    rainbowhat.rainbow.clear()
    for x in range(0,min(len(array),7)):
        if array[x] == 1:
            r,g,b = [1,1,1]  #gray
        elif array[x] == -1:
            r,g,b = [0,1,0]  #green
        elif array[x] == 2:
            r,g,b = [1,0,0]  #red
        elif array[x] == 3:
            r,g,b = [1,0,1]  #purple
#        elif array[x] == 4:
#            r,g,b = [0,1,1]  #lightblue
        else:
            r,g,b = blank
        rainbowhat.rainbow.set_pixel(6-x, r,g,b,brightness)
    try:
        bus.read_byte(112)         #check to see if rainbow hat is connected
        rainbowhat.rainbow.show()  #firing this code with unicornhathd connected breaks it
    except Exception:
        pass

def rainbow_show_float(vala):
    """write to four character display"""
    try:
        bus.read_byte(112)         #check to see if rainbow hat is connected
        rainbowhat.lights.red.off()    #hack for starting led
        rainbowhat.lights.green.off()    #hack for starting led
        rainbowhat.lights.blue.off()    #hack for starting led
        rainbowhat.display.clear()
        rainbowhat.display.print_float(vala)
        rainbowhat.display.show()
    except Exception:
        pass

def curve_hats_update(myfloat, booststatusarray, eth_price):
    """output to rainbow and microdot hats"""
    rainbow_show_float(myfloat)
    rainbow_show_boost_status(booststatusarray)
    microdotphat.set_clear_on_exit(False)
    microdotphat.set_rotate180(1)
    microdotphat.write_string(str(format(round(eth_price),',')).rjust(6), offset_x=0, kerning=False)
    microdotphat.show()
