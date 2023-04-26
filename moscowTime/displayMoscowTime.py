from color_setup import ssd
from gui.core.writer import Writer
from gui.core.nanogui import refresh
from gui.widgets.label import Label

import network
import moscowTime.secrets as secrets
import time
import urequests
import json


# Font
import gui.fonts.freesans70 as large

wri_large = Writer(ssd, large, verbose=False)
wri_large.set_clip(False, False, False)

# 296*128

def connectWIFI():
    wifi = network.WLAN(network.STA_IF)
    wifi.active(True)
    wifi.connect(secrets.SSID, secrets.PASSWORD)
    print(wifi.isconnected())
     
def getMoscowTime():
    data = urequests.get("https://price.bisq.wiz.biz/getAllMarketPrices").json()
    print(data['data'][49]['price']) 
    usdPrice = data['data'][49]['price']
    moscowTime = str(1 / float(usdPrice)*100000000)[0:4]
    print (moscowTime)
    return moscowTime

def main():
    connectWIFI()
    refresh(ssd, True)
    ssd.wait_until_ready()
    print("Timer start")
    time.sleep(180)
    print("Timer done")
    ssd._full = False
    ssd.wait_until_ready()
    refresh(ssd, True)
    row = 30
    col = 50
    ssd.wait_until_ready()
    ssd.sleep() #deep sleep
    print("deep sleep")
    time.sleep(25)
    i = 1
    while True:
        if i > 80:
            i = 1
            refresh(ssd, True)
            ssd.wait_until_ready()
            time.sleep(180)
            ssd._full = False
            refresh(ssd, True)
            time.sleep(25)
            
        print("i= "+str(i))
        print("label")
        Label(wri_large, row, col, getMoscowTime())
        refresh(ssd, False)
        ssd.wait_until_ready()
        ssd.sleep() #deep sleep
        time.sleep(600)
        i = i + 1 
main()
