from color_setup import ssd
from gui.core.writer import Writer
from gui.core.nanogui import refresh
from gui.widgets.label import Label

import time
import gui.fonts.orangeClockIcons25 as iconsSmall
import gui.fonts.orangeClockIcons35 as iconsLarge
import gui.fonts.libreFranklinBold60 as large
import gui.fonts.libreFranklinSemiBold29 as small


wri_iconsLarge = Writer(ssd, iconsLarge, verbose=False)
wri_iconsSmall = Writer(ssd, iconsSmall, verbose=False)
wri_large = Writer(ssd, large, verbose=False)
wri_small = Writer(ssd, small, verbose=False)


labelRow1 = 5
labelRow2 = 36
labelRow3 = 102

# Display 296*128
displayLength = 296
displayHeight = 128
blockHeight = "804618"  # A
moscowTime = "3784"  # E
mempoolFees = "L:8 M:8 H:9"  # C
dollarSats = "26,000"  # H


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
                + Writer.stringlen(wri_iconsSmall, "A")
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
                - Writer.stringlen(wri_iconsSmall, "A")
                - Writer.stringlen(wri_small, blockHeight)
                - 4
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
                displayLength
                - Writer.stringlen(wri_iconsLarge, "E")
                - Writer.stringlen(wri_large, moscowTime)
                - 4
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
                + 4
            )
            / 2
        ),
        mempoolFees,
    )
    Label(
        wri_iconsSmall,
        labelRow3 - 3,
        int(
            (
                displayLength
                - Writer.stringlen(wri_iconsSmall, "C")
                - Writer.stringlen(wri_small, mempoolFees)
                - 4
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
