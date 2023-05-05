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

labelMoscowTimeRow = 30
labelMoscowTimeCol = 50

def connectWIFI():
    wifi = network.WLAN(network.STA_IF)
    wifi.active(True)
    wifi.connect(secrets.SSID, secrets.PASSWORD)
    print(wifi.isconnected())
     
def getMoscowTime():
    data = urequests.get("https://price.bisq.wiz.biz/getAllMarketPrices").json()
    priceUSD = data['data'][49]['price']
    moscowTime = str(100000000 / float(priceUSD))[0:4]
    return moscowTime

def displayInit():
    refresh(ssd, True)
    ssd.wait_until_ready()
    time.sleep(180)
    ssd._full = False
    ssd.wait_until_ready()
    refresh(ssd, True)
    ssd.wait_until_ready()
    ssd.sleep() #deep sleep
    time.sleep(25)
         
def main():
    connectWIFI()
    displayInit()
    i = 1
    while True:
        if i > 80:
            i = 1
            ssd._full = True
            refresh(ssd, True)
            ssd.wait_until_ready()
            time.sleep(180)
            ssd._full = False
            refresh(ssd, True)
            time.sleep(25)
            
        Label(wri_large, labelMoscowTimeRow, labelMoscowTimeCol, getMoscowTime())
        refresh(ssd, False)
        ssd.wait_until_ready()
        ssd.sleep() 
        time.sleep(600)
        i = i + 1
        
main()
