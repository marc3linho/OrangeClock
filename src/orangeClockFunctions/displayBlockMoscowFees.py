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
import gui.fonts.libreFranklinBold60 as large
import gui.fonts.libreFranklinSemiBold29 as small
import gc

wri_iconsLarge = Writer(ssd, iconsLarge, verbose=False)
wri_iconsSmall = Writer(ssd, iconsSmall, verbose=False)
wri_large = Writer(ssd, large, verbose=False)
wri_small = Writer(ssd, small, verbose=False)

rowMaxDisplay = 296
labelRow1 = 5
labelRow2 = 36
labelRow3 = 98
symbolRow1 = "A"
symbolRow2 = "E"
symbolRow3 = "C"
secretsSSID = ""
secretsPASSWORD = ""

def connectWIFI():
    global wifi
    wifi = network.WLAN(network.STA_IF)
    wifi.active(True)
    wifi.connect(secretsSSID, secretsPASSWORD)
    time.sleep(1)
    print(wifi.isconnected())


def setSecrets(SSID, PASSWORD):
    global secretsSSID
    global secretsPASSWORD
    secretsSSID = SSID
    secretsPASSWORD = PASSWORD
    

def getPriceUSD():
    gc.collect()
    data = urequests.get("https://mempool.space/api/v1/prices")
    priceUSD = data.json()["USD"] #change USD to EUR for price in euro
    data.close()
    return priceUSD


def getMoscowTime():
    moscowTime = str(int(100000000 / float(getPriceUSD())))
    return moscowTime


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


def main():
    gc.enable()
    global wifi
    global secretsSSID
    global secretsPASSWORD
    print("===============debug id=1===============")
    print("memory use: ", gc.mem_alloc() / 1024, "KiB")
    print("memory free: ",gc.mem_free() / 1024, "KiB")
    print("===============end=debug===============")
    issue = False
    blockHeight = ""
    moscowTime = ""
    mempoolFees = ""
    i = 1
    connectWIFI()
    displayInit()
    while True:
        print("===============debug id=2===============")
        print("memory use: ", gc.mem_alloc() / 1024, "KiB")
        print("memory free: ",gc.mem_free() / 1024, "KiB")
        print("===============end=debug===============")
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
            symbolRow1 = "A"
            blockHeight = getLastBlock()
        except Exception as err:
            blockHeight = "connection error"
            symbolRow1 = ""
            print("Block: Handling run-time error:", err)
            print("===============debug id=2.1===============")
            print("memory use: ", gc.mem_alloc() / 1024, "KiB")
            print("memory free: ",gc.mem_free() / 1024, "KiB")
            print("===============end=debug===============")
            issue = True
        try:
            symbolRow2 = "E"
            moscowTime = getMoscowTime()
        except Exception as err:
            moscowTime = "error"
            symbolRow2 = ""
            print("Moscow: Handling run-time error:", err)
            print("===============debug id=2.2===============")
            print("memory use: ", gc.mem_alloc() / 1024, "KiB")
            print("memory free: ",gc.mem_free() / 1024, "KiB")
            print("===============end=debug===============")
            issue = True
        try:
            symbolRow3 = "C"
            mempoolFees = getMempoolFeesString()
        except Exception as err:
            mempoolFees = "connection error"
            symbolRow3 = ""
            print("Fees: Handling run-time error:", err)
            print("===============debug id=2.1===============")
            print("memory use: ", gc.mem_alloc() / 1024, "KiB")
            print("memory free: ",gc.mem_free() / 1024, "KiB")
            print("===============end=debug===============")
            issue = True
        if wifi.isconnected():
            refresh(ssd, True)
            ssd.wait_until_ready()
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
        )

        Label(
            wri_iconsSmall,
            labelRow1 + 2, # center icon with text
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
        )
        Label(
            wri_large,
            labelRow2,
            int(
                (
                    rowMaxDisplay
                    - Writer.stringlen(wri_large, moscowTime)
                    + Writer.stringlen(wri_iconsLarge, symbolRow2)
                    + 2 # spacing
                )
                / 2
            ),
            moscowTime,
        )
        Label(
            wri_iconsLarge, 
            labelRow2 + 7, # + 10 for centered satsymbol
            int(
                (
                    rowMaxDisplay
                    - Writer.stringlen(wri_iconsLarge, symbolRow2)
                    - Writer.stringlen(wri_large, moscowTime)
                    - 2 # spacing
                )
                / 2
            ),
            symbolRow2,
        )
        Label(
            wri_small,
            labelRow3,
            int(
                (
                    rowMaxDisplay
                    - Writer.stringlen(wri_small, mempoolFees)
                    + Writer.stringlen(wri_iconsSmall, symbolRow3)
                    + 4 # spacing
                )
                / 2
            ),
            mempoolFees,
        )
        Label(
            wri_iconsSmall,
            labelRow3 + 1, # center icon with text
            int(
                (
                    rowMaxDisplay
                    - Writer.stringlen(wri_iconsSmall, symbolRow3)
                    - Writer.stringlen(wri_small, mempoolFees)
                    - 4 # spacing
                )
                / 2
            ),
            symbolRow3,
        )

        refresh(ssd, False)
        ssd.wait_until_ready()
        ssd.sleep()
        if not issue:
            time.sleep(600) #600 normal
        else:
            wifi.disconnect()
            print("===============debug id=3===============")
            print("memory use: ", gc.mem_alloc() / 1024, "KiB")
            print("memory free: ",gc.mem_free() / 1024, "KiB")
            print("===============end=debug===============")
            wifi.connect(secretsSSID, secretsPASSWORD)
            time.sleep(60)
            gc.collect()

        i = i + 1


