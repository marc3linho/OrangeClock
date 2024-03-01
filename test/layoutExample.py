from color_setup import ssd
from gui.core.writer import Writer
from gui.core.nanogui import refresh
from gui.widgets.label import Label

import time
import gui.fonts.orangeClockIcons25 as iconsSmall
import gui.fonts.orangeClockIcons35 as iconsLarge
import gui.fonts.libreFranklinBold50 as large
import gui.fonts.libreFranklinSemiBold29 as small


wri_iconsLarge = Writer(ssd, iconsLarge, verbose=False)
wri_iconsSmall = Writer(ssd, iconsSmall, verbose=False)
wri_large = Writer(ssd, large, verbose=False)
wri_small = Writer(ssd, small, verbose=False)


labelRow1 = 5
labelRow2 = 42
labelRow3 = 98

# Display 296*128
displayLength = 296
displayHeight = 128
symbolRow1 = "A"
symbolRow2 = "L"
symbolRow3 = "F"
blockHeight = "823376"  # A
moscowTime = "1779"  # L
mempoolFees = "L:89 M:99 H:109"  # F
dollarSats = "100,000"  # E

def main():
    refresh(ssd, True)
    ssd.wait_until_ready()
    # time.sleep(10)
    Label(
        wri_small,
        labelRow1,
        int(
            (
                displayLength
                - Writer.stringlen(wri_small, blockHeight)
                + Writer.stringlen(wri_iconsSmall, symbolRow1)
                + 4
            )
            / 2
        ),
        blockHeight,
    )

    Label(
        wri_iconsSmall,
        labelRow1 + 2,
        int(
            (
                displayLength
                - Writer.stringlen(wri_iconsSmall, symbolRow1)
                - Writer.stringlen(wri_small, blockHeight)
                - 4
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
                displayLength
                - Writer.stringlen(wri_large, moscowTime)
                + Writer.stringlen(wri_iconsLarge, symbolRow2)
                + 2  # spacing
            )
            / 2
        ),
        moscowTime,
    )
    Label(
        wri_iconsLarge,
        labelRow2 + 1, #+ 7 for centered satsymbol
        int(
            (
                displayLength
                - Writer.stringlen(wri_iconsLarge, symbolRow2)
                - Writer.stringlen(wri_large, moscowTime)
                - 2  # spacing
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
                displayLength
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
        labelRow3 + 1,
        int(
            (
                displayLength
                - Writer.stringlen(wri_iconsSmall, symbolRow3)
                - Writer.stringlen(wri_small, mempoolFees)
                - 4
            )
            / 2
        ),
        symbolRow3,
    )

    ssd.wait_until_ready()
    refresh(ssd, False)
    ssd.wait_until_ready()
    ssd.sleep()
    print("sleep")


main()
