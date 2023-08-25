from color_setup import ssd
from gui.core.writer import Writer
from gui.core.nanogui import refresh
from gui.widgets.label import Label

import network
import orangeClockFunctions.secrets as secrets
import time
import urequests
import json
import gui.fonts.orangeClockIcons25 as iconsSmall
import gui.fonts.orangeClockIcons35 as iconsLarge
import gui.fonts.libreFranklinBold60 as large
import gui.fonts.libreFranklinSemiBold29 as small

wri_iconsLarge = Writer(ssd, iconsLarge, verbose=False)
wri_iconsSmall = Writer(ssd, iconsSmall, verbose=False)
wri_large = Writer(ssd, large, verbose=False)
wri_small = Writer(ssd, small, verbose=False)

rowMaxDisplay = 296
labelRow1 = 5
labelRow2 = 36
labelRow3 = 102
symbolRow1 = "A"
symbolRow2 = "E"
symbolRow3 = "C"


def connectWIFI():
    global wifi
    wifi = network.WLAN(network.STA_IF)
    wifi.active(True)
    wifi.connect(secrets.SSID, secrets.PASSWORD)
    time.sleep(1)
    print(wifi.isconnected())


def getPriceUSD():
    data = urequests.get("https://price.bisq.wiz.biz/getAllMarketPrices")
    jsonData = data.json()
    data.close()
    priceUSD = jsonData["data"][49]["price"]
    return priceUSD


def getMoscowTime():
    moscowTime = str(int(100000000 / float(getPriceUSD())))
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
    time.sleep(20)
    ssd._full = False
    ssd.wait_until_ready()
    refresh(ssd, True)
    ssd.wait_until_ready()
    ssd.sleep()  # deep sleep
    time.sleep(25)


def main():
    global wifi
    issue = False
    blockHeight = ""
    moscowTime = ""
    mempoolFees = ""
    i = 1
    connectWIFI()
    displayInit()
    while True:
        if issue:
            issue = False
        if i > 72:
            i = 1
            refresh(ssd, True)  # awake from deep sleep
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
        try:
            symbolRow1 = "A"
            blockHeight = getLastBlock()
        except Exception as err:
            blockHeight = "connection error"
            symbolRow1 = ""
            print("Block: Handling run-time error:", err)
            issue = True
        try:
            symbolRow2 = "E"
            moscowTime = getMoscowTime()
        except Exception as err:
            moscowTime = "error"
            symbolRow2 = ""
            print("Moscow: Handling run-time error:", err)
            issue = True
        try:
            symbolRow3 = "C"
            mempoolFees = getMempoolFeesString()
        except Exception as err:
            mempoolFees = "connection error"
            symbolRow3 = ""
            print("Fees: Handling run-time error:", err)
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
            labelRow1 + 2, #center icon with text
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
                    + 4
                )
                / 2
            ),
            moscowTime,
        )
        Label(
            wri_iconsLarge,
            labelRow2,
            int(
                (
                    rowMaxDisplay
                    - Writer.stringlen(wri_iconsLarge, symbolRow2)
                    - Writer.stringlen(wri_large, moscowTime)
                    - 4
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
                    + 4
                )
                / 2
            ),
            mempoolFees,
        )
        Label(
            wri_iconsSmall,
            labelRow3 - 3, #center icon with text
            int(
                (
                    rowMaxDisplay
                    - Writer.stringlen(wri_iconsSmall, symbolRow3)
                    - Writer.stringlen(wri_small, mempoolFees)
                    - 4
                )
                / 2
            ),
            symbolRow3,
        )

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
