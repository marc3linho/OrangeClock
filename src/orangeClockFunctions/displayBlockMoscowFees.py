from color_setup import ssd
from gui.core.writer import Writer
from gui.core.nanogui import refresh
from gui.widgets.label import Label

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

wri_iconsLarge = Writer(ssd, iconsLarge, verbose=False)
wri_iconsSmall = Writer(ssd, iconsSmall, verbose=False)
wri_large = Writer(ssd, large, verbose=False)
wri_small = Writer(ssd, small, verbose=False)

rowMaxDisplay = 296
labelRow1 = 5
labelRow2 = 44
labelRow3 = 98
symbolRow1 = "A"
symbolRow2 = "L"
symbolRow3 = "F"
secretsSSID = ""
secretsPASSWORD = ""
dispVersion1 = "bh"  #bh = block height / hal = halving countdown / zap = Nostr zap counter
dispVersion2 = "mts" #mts = moscow time satsymbol / mts2 = moscow time satusd icon / mt = without satsymbol / fp1 = fiat price [$] / fp2 = fiat price [€]
dispVersion3 = "fees"    #fees = mempool fees / fp7 = JPY
npub = ""

def connectWIFI():
    global wifi
    wifi = network.WLAN(network.STA_IF)
    wifi.active(True)
    wifi.connect(secretsSSID, secretsPASSWORD)
    time.sleep(1)
    print(wifi.isconnected())


def setSelectDisplay(displayVersion1, nPub, displayVersion2, displayVersion3):
    global dispVersion1
    global dispVersion2
    global dispVersion3
    global npub
    dispVersion1 = displayVersion1
    npub = nPub
    dispVersion2 = displayVersion2
    dispVersion3 = displayVersion3


def setSecrets(SSID, PASSWORD):
    global secretsSSID
    global secretsPASSWORD
    secretsSSID = SSID
    secretsPASSWORD = PASSWORD


def getPrice(currency):
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
    if currency == "CHF":
        price_str = price_str.replace(",", " ")
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
            elif dispVersion2 == "fp3":
                symbolRow2 = "C"
                textRow2 = getPriceDisplay("GBP")
            elif dispVersion2 == "fp4":
                symbolRow2 = "B"
                textRow2 = getPriceDisplay("CAD")
            elif dispVersion2 == "fp5":
                symbolRow2 = ""
                textRow2 = "Fr. "+getPriceDisplay("CHF")
            elif dispVersion2 == "fp6":
                symbolRow2 = "B"
                textRow2 = getPriceDisplay("AUD")  
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
            if dispVersion3 == "fp7":
                #symbolRow3 = "D"
                #mempoolFees = getPrice("JPY")
                print("fp7")
            else:
                symbolRow3 = "F"
                mempoolFees = getMempoolFeesString()
        except Exception as err:
            mempoolFees = "connection error"
            symbolRow3 = ""
            print("Fees: Handling run-time error:", err)
            debugConsoleOutput("5")
            issue = True

        labels = [
            Label(
                wri_small,
                labelRow1,
                int(
                    (
                        rowMaxDisplay
                        - Writer.stringlen(wri_small, blockHeight)
                        + Writer.stringlen(wri_iconsSmall, symbolRow1)
                        + 4  # spacing
                    )
                    / 2
                ),
                blockHeight,
            ),
            Label(
                wri_iconsSmall,
                labelRow1 + 2,  # center icon with text
                int(
                    (
                        rowMaxDisplay
                        - Writer.stringlen(wri_iconsSmall, symbolRow1)
                        - Writer.stringlen(wri_small, blockHeight)
                        - 4  # spacing
                    )
                    / 2
                ),
                symbolRow1,
            ),
            Label(
                wri_large,
                labelRow2,
                int(
                    (
                        rowMaxDisplay
                        - Writer.stringlen(wri_large, textRow2)
                        + Writer.stringlen(wri_iconsLarge, symbolRow2)
                        # + 2  # spacing
                    )
                    / 2
                ),
                textRow2,
            ),
            Label(
                wri_iconsLarge,
                labelRow2,  # + 10 for centered satsymbol
                int(
                    (
                        rowMaxDisplay
                        - Writer.stringlen(wri_iconsLarge, symbolRow2)
                        - Writer.stringlen(wri_large, textRow2)
                        # - 2  # spacing
                    )
                    / 2
                ),
                symbolRow2,
            ),
            Label(
                wri_small,
                labelRow3,
                int(
                    (
                        rowMaxDisplay
                        - Writer.stringlen(wri_small, mempoolFees)
                        + Writer.stringlen(wri_iconsSmall, symbolRow3)
                        + 4  # spacing
                    )
                    / 2
                ),
                mempoolFees,
            ),
            Label(
                wri_iconsSmall,
                labelRow3 + 1,  # center icon with text
                int(
                    (
                        rowMaxDisplay
                        - Writer.stringlen(wri_iconsSmall, symbolRow3)
                        - Writer.stringlen(wri_small, mempoolFees)
                        - 4  # spacing
                    )
                    / 2
                ),
                symbolRow3,
            )
        ]

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

