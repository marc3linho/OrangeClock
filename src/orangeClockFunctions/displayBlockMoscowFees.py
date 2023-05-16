from color_setup import ssd
from gui.core.writer import Writer
from gui.core.nanogui import refresh
from gui.widgets.label import Label

import network
import orangeClockFunctions.secrets as secrets
import time
import urequests
import json

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
labelMoscowTimeCol = 45
labelBlockRow = 5
labelBlockCol = 75
labelFeeRow = 110
labelFeeCol = 40


def connectWIFI():

    global wifi
    wifi = network.WLAN(network.STA_IF)
    wifi.active(True)
    wifi.connect(secrets.SSID, secrets.PASSWORD)
    time.sleep(1)
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
    jsonData = data.json()
    data.close()
    return jsonData

def getMempoolFeesString():
    mempoolFees = getMempoolFees()
    mempoolFeesString = "Fees[sat/vB] L:" + str(mempoolFees["hourFee"])+" M:"+str(mempoolFees["halfHourFee"])+" H:"+str(mempoolFees["fastestFee"])
    return mempoolFeesString

def displayInit():
    refresh(ssd, True)
    ssd.wait_until_ready()
    time.sleep(120)
    ssd._full = False
    ssd.wait_until_ready()
    refresh(ssd, True)
    ssd.wait_until_ready()
    ssd.sleep() #deep sleep
    time.sleep(25)
        
def main():
    global wifi
    issue = False
    i = 1
    
    connectWIFI()
    displayInit()
    
    while True:
        if issue:
            issue = False 
        if i > 72:
            i = 1
            refresh(ssd, True) #awake from deep sleep 
            time.sleep(25)
            ssd._full = True 
            ssd.wait_until_ready()
            refresh(ssd, True)
            ssd.wait_until_ready()
            time.sleep(120)
            ssd._full = False
            ssd.wait_until_ready()
            refresh(ssd, True)
            time.sleep(25)
        if wifi.isconnected():
            refresh(ssd, True)    
        try:
            Label(wri_small, labelBlockRow, labelBlockCol, "Block: " + getLastBlock())      
        except Exception as err:
            Label(wri_small, labelBlockRow, labelBlockCol, "connection issue")
            print('Block: Handling run-time error:', err)
            issue = True
        try:    
            Label(wri_large, labelMoscowTimeRow, labelMoscowTimeCol, getMoscowTime())
        except Exception as err:
            Label(wri_small, labelMoscowTimeRow, labelMoscowTimeCol, "connection issue")
            print('Moscow: Handling run-time error:', err)
            issue = True
        try:    
            Label(wri_tiny, labelFeeRow, labelFeeCol, getMempoolFeesString())
        except Exception as err:
            Label(wri_tiny, labelFeeRow, labelFeeCol, "connection issue")
            print('Fees: Handling run-time error:', err)
            issue = True
        refresh(ssd, False)
        ssd.wait_until_ready()
        ssd.sleep() 
        if not issue:
            time.sleep(600)
        else:
            wifi.disconnect()
            wifi.connect(secrets.SSID, secrets.PASSWORD)
            time.sleep(60)            
            
        i = i + 1
        
main()