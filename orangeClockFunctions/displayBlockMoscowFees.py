from color_setup import ssd
from gui.core.writer import Writer
from gui.core.nanogui import refresh
from gui.widgets.label import Label

import network
import orangeClockFunctions.secrets as secrets
import time
import urequests
import json


# Font
import gui.fonts.freesans70 as large
import gui.fonts.freesans20 as small
import gui.fonts.freesans15 as tiny

wri_large = Writer(ssd, large, verbose=False)
wri_large.set_clip(False, False, False)
wri_small = Writer(ssd, small, verbose=False)
wri_small.set_clip(False, False, False)
wri_tiny = Writer(ssd, tiny, verbose=False)
wri_tiny.set_clip(False, False, False)

labelMoscowTimeRow = 30
labelMoscowTimeCol = 50
labelBlockRow = 5
labelBlockCol = 75
labelFeeRow = 110
labelFeeCol = 15

def connectWIFI():
    wifi = network.WLAN(network.STA_IF)
    wifi.active(True)
    wifi.connect(secrets.SSID, secrets.PASSWORD)
    print(wifi.isconnected())
     
def getMoscowTime():
    data = urequests.get("https://price.bisq.wiz.biz/getAllMarketPrices")
    jsonData = data.json()
    priceUSD = jsonData['data'][49]['price']
    moscowTime = str(100000000 / float(priceUSD))[0:4]
    data.close()
    return moscowTime

def getLastBlock():
    data = urequests.get("https://mempool.space/api/blocks/tip/height")
    block = data.text
    data.close()
    return block

def getMempoolFees():
    data = urequests.get("https://mempool.space/api/v1/fees/recommended")
    block = data.text
    data.close()
    return block

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
        if i > 72:
            i = 1
            ssd._full = True
            ssd.wait_until_ready()
            refresh(ssd, True)
            ssd.wait_until_ready()
            time.sleep(180)
            ssd._full = False
            ssd.wait_until_ready()
            refresh(ssd, True)
            time.sleep(25)

        Label(wri_small, labelBlockRow, labelBlockCol, "Block: " + getLastBlock())      
        Label(wri_large, labelMoscowTimeRow, labelMoscowTimeCol, getMoscowTime())
        Label(wri_tiny, labelFeeRow, labelFeeCol, "L:126 sat/vB M:153 sat/vB H:165 sat/vB")
        refresh(ssd, False)
        ssd.wait_until_ready()
        ssd.sleep() 
        time.sleep(600)
        i = i + 1
        
main()