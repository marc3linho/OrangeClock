rom color_setup import ssd
from gui.core.writer import Writer
from gui.core.nanogui import refresh
from gui.widgets.label import Label

import time
import gui.fonts.orangeClockIcons24 as iconsSmall
import gui.fonts.orangeClockIcons44 as iconsLarge
import gui.fonts.libreFranklinBold56 as large
import gui.fonts.libreFranklinBold24 as small


wri_iconsLarge = Writer(ssd, iconsLarge, verbose=False)
wri_iconsSmall = Writer(ssd, iconsSmall, verbose=False)
wri_large = Writer(ssd, large, verbose=False)
wri_small = Writer(ssd, small, verbose=False)


labelRow1 = 5
labelRow2 = 40
labelRow3 = 100

# Display 296*128
displayLength = 296
displayHeight = 128
blockHeight = "804480" #A
moscowTime = "383" #D
mempoolFees = "L:8 M:9 H:10" #C
dollarSats = "26,000" #H        


def main():
    refresh(ssd, True)
    ssd.wait_until_ready()
    #time.sleep(10)
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
    Label(
        wri_small,
        labelRow3,
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
        labelRow3,
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
            
    ssd.wait_until_ready()
    refresh(ssd, False)
    ssd.wait_until_ready()
    ssd.sleep()
    print("sleep")

main()

