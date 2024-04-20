from color_setup import ssd
from gui.core.nanogui import refresh
from orangeClockFunctions.compositors import composeClock

import network
import time
import urequests
import json
import gui.fonts.orangeClockIcons25 as iconsSmall
import gui.fonts.orangeClockIcons35 as iconsLarge
import gui.fonts.libreFranklinBold50 as large
import gui.fonts.libreFranklinSemiBold29 as small
import gc
import math

symbolRow1 = "A"
symbolRow2 = "L"
symbolRow3 = "F"
secretsSSID = ""
secretsPASSWORD = ""
dispVersion1 = "bh"  #bh = block height / hal = halving countdown / zap = Nostr zap counter
dispVersion2 = "mts" #mts = moscow time satsymbol / mts2 = moscow time satusd icon / mt = without satsymbol / fp1 = fiat price [$] / fp2 = fiat price [€]
npub = ""

def connectWIFI():
    global wifi
    wifi = network.WLAN(network.STA_IF)
    wifi.active(True)
    wifi.connect(secretsSSID, secretsPASSWORD)
    time.sleep(1)
    print(wifi.isconnected())


def setSelectDisplay(displayVersion1, nPub, displayVersion2):
    global dispVersion1
    global dispVersion2
    global npub
    dispVersion1 = displayVersion1
    npub = nPub
    dispVersion2 = displayVersion2


def setSecrets(SSID, PASSWORD):
    global secretsSSID
    global secretsPASSWORD
    secretsSSID = SSID
    secretsPASSWORD = PASSWORD


def getPrice(currency): # change USD to EUR for price in euro
    gc.collect()
    data = urequests.get("https://mempool.space/api/v1/prices")
    price = data.json()[currency]
    data.close()
    return price


def getMoscowTime():
    moscowTime = str(int(100000000 / float(getPrice("USD"))))
    return moscowTime


def getPriceDisplay(currency):
    price_str = f"{getPrice(currency):,}"
    if currency == "EUR":
        price_str = price_str.replace(",", ".")
    return price_str


def getLastBlock():
    gc.collect()
    data = urequests.get("https://mempool.space/api/blocks/tip/height")
    block = data.text
    data.close()
    return block


def getMempoolFees():
    gc.collect()
    data = urequests.get("https://mempool.space/api/v1/fees/recommended")
    jsonData = data.json()
    data.close()
    return jsonData


def getMempoolFeesString():
    mempoolFees = getMempoolFees()
    mempoolFeesString = (
        "L:"
        + str(mempoolFees["hourFee"])
        + " M:"
        + str(mempoolFees["halfHourFee"])
        + " H:"
        + str(mempoolFees["fastestFee"])
    )
    return mempoolFeesString


def getNostrZapCount(nPub):
    gc.collect()
    data = urequests.get("https://api.nostr.band/v0/stats/profile/"+nPub)
    jsonData = str(data.json()["stats"][str(data.json())[12:76]]["zaps_received"]["count"])
    data.close()
    return jsonData


def getNextHalving():
    return str(210000 * (math.trunc(int(getLastBlock()) / 210000) + 1) - int(getLastBlock()))


def displayInit():
    refresh(ssd, True)
    ssd.wait_until_ready()
    time.sleep(5)
    ssd._full = False
    ssd.wait_until_ready()
    refresh(ssd, True)
    ssd.wait_until_ready()
    ssd.sleep()  # deep sleep
    time.sleep(5)


def debugConsoleOutput(id):
    print("===============debug id= " + id + "===============")
    print("memory use: ", gc.mem_alloc() / 1024, "KiB")
    print("memory free: ", gc.mem_free() / 1024, "KiB")
    print("===============end debug===============")


def main():
    gc.enable()
    global wifi
    global secretsSSID
    global secretsPASSWORD
    debugConsoleOutput("1")
    issue = False
    blockHeight = ""
    textRow2 = ""
    mempoolFees = ""
    i = 1
    connectWIFI()
    displayInit()
    while True:
        debugConsoleOutput("2")
        if issue:
            issue = False
        if i > 72:
            i = 1
            refresh(ssd, True)  # awake from deep sleep
            time.sleep(5)
            ssd._full = True
            ssd.wait_until_ready()
            refresh(ssd, True)
            ssd.wait_until_ready()
            time.sleep(20)
            ssd._full = False
            ssd.wait_until_ready()
            refresh(ssd, True)
            time.sleep(5)
        try:
            if dispVersion1 == "zap":
                symbolRow1 = "I"
                blockHeight = getNostrZapCount(npub)
            elif dispVersion1 == "hal":
                symbolRow1 = "H"
                blockHeight = getNextHalving()
            else:
                symbolRow1 = "A"
                blockHeight = getLastBlock()    
        except Exception as err:
            blockHeight = "connection error"
            symbolRow1 = ""
            print("Block: Handling run-time error:", err)
            debugConsoleOutput("3")
            issue = True
        try:
            if dispVersion2 == "mt":
                symbolRow2 = ""
                textRow2 = getMoscowTime()
            elif dispVersion2 == "mts2":
                symbolRow2 = "M"
                textRow2 = getMoscowTime()
            elif dispVersion2 == "fp1":
                symbolRow2 = "E"
                textRow2 = getPriceDisplay("USD")
            elif dispVersion2 == "fp2":
                symbolRow2 = "B"
                textRow2 = getPriceDisplay("EUR")
            else:
                symbolRow2 = "L"
                textRow2 = getMoscowTime()        
        except Exception as err:
            textRow2 = "error"
            symbolRow2 = ""
            print("Moscow: Handling run-time error:", err)
            debugConsoleOutput("4")
            issue = True
        try:
            symbolRow3 = "F"
            mempoolFees = getMempoolFeesString()
        except Exception as err:
            mempoolFees = "connection error"
            symbolRow3 = ""
            print("Fees: Handling run-time error:", err)
            debugConsoleOutput("5")
            issue = True

        labels = composeClock(
            ssd,
            (blockHeight, symbolRow1),
            (textRow2, symbolRow2),
            (mempoolFees, symbolRow3)
        )

        refresh(ssd, False)
        ssd.wait_until_ready()
        ssd.sleep()
        if not issue:
            time.sleep(600)  # 600 normal

        else:
            wifi.disconnect()
            debugConsoleOutput("6")
            wifi.connect(secretsSSID, secretsPASSWORD)
            time.sleep(60)
            gc.collect()

        # Have the Labels write blanks into the framebuf to erase what they
        # rendered in the previous cycle.
        for label in labels:
            label.value("")
            
        i = i + 1
