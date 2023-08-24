from math import pi, sin
from color_setup import ssd
from gui.core.writer import Writer
from gui.core.nanogui import refresh
from gui.widgets.label import Label
from gui.widgets.textbox import Textbox

import time
import gui.fonts.orangeClockIcons24 as iconsSmall
import gui.fonts.orangeClockIcons44 as iconsLarge
import gui.fonts.libreFranklinBold56 as large
import gui.fonts.libreFranklinBold24 as small
import gui.fonts.freesans15 as tiny
import gui.fonts.freesansFake as fake

wri_iconsLarge = Writer(ssd, iconsLarge, verbose=False)
wri_iconsSmall = Writer(ssd, iconsSmall, verbose=False)
wri_large = Writer(ssd, large, verbose=False)
wri_small = Writer(ssd, small, verbose=False)
wri_tiny = Writer(ssd, tiny, verbose=False)
wri_fake = Writer(ssd, fake, verbose=False)


labelRow1 = 5
labelCol1 = 75
labelRow2 = 30
labelCol2 = 45
labelRow3 = 110
labelCol3 = 40
# Display 296*128
displayLength = 296
displayHeight = 128
blockHeight = "803724" #A
moscowTime = "3773" #D
mempoolFees = "L:9 M:11 H:14" #C
clearTop = "                  "
clearMid = "              "
dollarSats = "26,000" #H        

def clearScreen():
    ssd.wait_until_ready()
    txt_test = Textbox(wri_fake, 0, 0, 290, 126, fgcolor=1, bgcolor=0, bdcolor=0)
    txt_test.show()
#         Label(
#                 wri_small,
#                 labelRow1,
#                 int(
#                     (
#                         displayLength
#                         - Writer.stringlen(wri_small, clearTop)
#                      )
#                      / 2
#                 ),
#                 clearTop,
#         )
#         Label(
#                 wri_large,
#                 labelRow2,
#                 int(
#                     (
#                         displayLength
#                         - Writer.stringlen(wri_large, clearMid)
#                     )
#                     / 2
#                 ),
#                 clearMid,
#         )
            
def main():
    print("Length blockHeight: " + str(Writer.stringlen(wri_large, blockHeight)))
    print("Length moscowTime: " + str(Writer.stringlen(wri_small, moscowTime)))
    print("Length mempoolFees: " + str(Writer.stringlen(wri_tiny, mempoolFees)))
    refresh(ssd, True)
    ssd.wait_until_ready()
    time.sleep(10)
    ssd._full = False
    ssd.wait_until_ready()
    refresh(ssd, True)
    i = 1
    while True:
        if i % 2 == 0:
            clearScreen()
            Label(
                wri_small,
                labelRow1,
                int(
                    (
                        displayLength
                        - Writer.stringlen(wri_small, blockHeight)
                        + Writer.stringlen(wri_iconsSmall, "A")
                     )
                     / 2
                ),
                blockHeight,
            )
            Label(
                wri_iconsSmall,
                labelRow1,
                int(
                    (
                        displayLength
                        - Writer.stringlen(wri_iconsSmall, "A")
                        - Writer.stringlen(wri_small, blockHeight )
                     )
                     / 2
                ),
                "A",
            )
            Label(
                wri_large,
                labelRow2,
                int(
                    (
                        displayLength
                        - Writer.stringlen(wri_large, moscowTime)
                        + Writer.stringlen(wri_iconsLarge, "E")
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
                        displayLength
                        - Writer.stringlen(wri_iconsLarge, "E")
                        - Writer.stringlen(wri_large, moscowTime)
                    )
                    / 2
                ),
                "E",
            )
        
        else:
            clearScreen()
            Label(
                wri_small,
                labelRow1,
                int(
                    (
                        displayLength
                        - Writer.stringlen(wri_small, mempoolFees)
                        + Writer.stringlen(wri_iconsSmall, "C")
                     )
                     / 2
                ),
                mempoolFees,
            )
            Label(
                wri_iconsSmall,
                labelRow1,
                int(
                    (
                        displayLength
                        - Writer.stringlen(wri_iconsSmall, "C")
                        - Writer.stringlen(wri_small, mempoolFees)
                     )
                     / 2
                ),
                "C",
            )
            
            #Label(
            #    wri_small,
            #    labelRow1,
            #    int((displayLength - Writer.stringlen(wri_small, mempoolFees)) / 2),
            #    mempoolFees,
            #)
            Label(
                wri_large,
                labelRow2,
                int(
                    (
                        displayLength
                        - Writer.stringlen(wri_large, dollarSats)
                        + Writer.stringlen(wri_iconsLarge, "H")
                    )
                    / 2
                ),
                dollarSats,
            )
            Label(
                wri_iconsLarge,
                labelRow2,
                int(
                    (
                        displayLength
                        - Writer.stringlen(wri_iconsLarge, "H")
                        - Writer.stringlen(wri_large, dollarSats)
                    )
                    / 2
                ),
                "H",
            )
        ssd.wait_until_ready()
        refresh(ssd, False)
        ssd.wait_until_ready()
        #ssd.sleep()
        print("i: "+str(i))
        time.sleep(20)
        i = i + 1

main()
