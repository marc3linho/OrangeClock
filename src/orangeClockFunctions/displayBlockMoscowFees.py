from color_setup import ssd
from gui.core.writer import Writer
from gui.core.nanogui import refresh
from gui.widgets.label import Label
from orangeClockFunctions.logging import log_exception
from orangeClockFunctions import datastore

import network
import time
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
spaceRow3 = 4
warningIcon = "R"
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


def setSecrets(SSID, PASSWORD, mempool_url):
    global secretsSSID
    global secretsPASSWORD
    global mempool
    secretsSSID = SSID
    secretsPASSWORD = PASSWORD
    mempool = mempool_url


def getMoscowTime():
    return str(int(100000000 / float(datastore.get_price("USD"))))


def getPriceDisplay(currency):
    price_str = f"{datastore.get_price(currency):,}"
    if currency == "EUR":
        price_str = price_str.replace(",", ".")
    return price_str


def getLastBlock():
    return str(datastore.get_height())


def getMempoolFeesString():
    def build_fees_string(mempoolFees, labels=True, halfHourFee=True):
        key_label_tuples = (
            ("hourFee", "L"),
            ("halfHourFee","M"),
            ("fastestFee","H")
        )
        fees = []
        for key, label in key_label_tuples:
            if key == "halfHourFee" and not halfHourFee:
                continue
            if labels:
                fees.append(label + ":" + str(mempoolFees[key]))
            else:
                fees.append(str(mempoolFees[key]))
        separator = " - " if len(fees) == 2 else "  "
        return separator.join(fees)

    mempoolFees = datastore.get_fees_dict()

    # width_of_screen - fees_icon - fees_space
    max_width = rowMaxDisplay - wri_iconsSmall.stringlen(symbolRow3) - spaceRow3

    answer = build_fees_string(mempoolFees)
    if wri_small.stringlen(answer) > max_width:
        # too big, try w/o medium-priority fees
        answer = build_fees_string(mempoolFees, halfHourFee=False)
    if wri_small.stringlen(answer) > max_width:
        # too big, try w/o "L:", "M:", and "H:" labels
        answer = build_fees_string(mempoolFees, labels=False)
    if wri_small.stringlen(answer) > max_width:
        # too big, try w/o labels and w/o medium-priority fees
        answer = build_fees_string(mempoolFees, labels=False, halfHourFee=False)

    return answer


def getNostrZapCount():
    return str(datastore.get_nostr_zap_count())


def getNextHalving():
    return str(210000 - datastore.get_height() % 210000)


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
    mem_alloc = gc.mem_alloc()
    print("=============== debug id=" + id + " ===============")
    print("memory used: ", mem_alloc / 1024, "KiB")
    print("memory free: ", gc.mem_free() / 1024, "KiB")
    gc.collect()
    print("gc.collect() freed additional:", (mem_alloc - gc.mem_alloc()) / 1024, "KiB")
    print("=============== end debug ===============")


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

    datastore.initialize(mempool)
    if npub:
        datastore.set_nostr_pubkey(npub)

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
            # alternatively: can avoid using raise_on_falure paramater
            # and instead call datastore.list_stale() for a list of stale data.
            new_data = datastore.refresh(raise_on_failure=True)
            if new_data:
                print("datastore.refresh() had updates: {}".format(",".join(new_data)))
        except Exception as err:
            log_exception(err)
            debugConsoleOutput("datastore.refresh() failure")
            print(err)
            issue = True
        try:
            if dispVersion1 == "zap":
                symbolRow1 = "I"
                blockHeight = getNostrZapCount()
            elif dispVersion1 == "hal":
                symbolRow1 = "H"
                blockHeight = getNextHalving()
            else:
                symbolRow1 = "A"
                blockHeight = getLastBlock()    
        except Exception as err:
            log_exception(err)
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
            log_exception(err)
            textRow2 = "error"
            symbolRow2 = ""
            print("Moscow: Handling run-time error:", err)
            debugConsoleOutput("4")
            issue = True
        try:
            symbolRow3 = "F"
            mempoolFees = getMempoolFeesString()
        except Exception as err:
            log_exception(err)
            mempoolFees = "connection error"
            symbolRow3 = ""
            print("Fees: Handling run-time error:", err)
            debugConsoleOutput("5")
            issue = True

        labels = []
        if issue:
            # warning-icon in upper-left corner to indicate error(s)
            labels.append(Label(wri_iconsSmall, 0, 0, warningIcon))
        labels += [
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
                        + spaceRow3  # spacing
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
                        - spaceRow3  # spacing
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
