from color_setup import ssd
from gui.core.writer import Writer
from gui.core.nanogui import refresh
from gui.widgets.label import Label

import gui.fonts.satoshiSymbol70 as satoshi
import gui.fonts.freesans70 as large
import gui.fonts.freesans20 as small
import gui.fonts.freesans15 as tiny

wri_satoshi = Writer(ssd, satoshi, verbose=False)
wri_large = Writer(ssd, large, verbose=False)
wri_small = Writer(ssd, small, verbose=False)
wri_tiny = Writer(ssd, tiny, verbose=False)

labelRow1 = 5
labelCol1 = 75
labelRow2 = 30
labelCol2 = 45
labelRow3 = 110
labelCol3 = 40
# Display 296*128
displayLength = 296
displayHeight = 128
blockHeight = "Block: 803724"
moscowTime = "3773"
satoshiSymbol = "1"
mempoolFees = "Fees[sat/vB] L:9 M:11 H:14"


def main():
    print("Length blockHeight: " + str(Writer.stringlen(wri_large, blockHeight)))
    print("Length moscowTime: " + str(Writer.stringlen(wri_small, moscowTime)))
    print("Length mempoolFees: " + str(Writer.stringlen(wri_tiny, mempoolFees)))
    refresh(ssd, True)
    ssd.wait_until_ready()
    Label(
        wri_small,
        labelRow1,
        int((displayLength - Writer.stringlen(wri_small, blockHeight)) / 2),
        blockHeight,
    )
    Label(
        wri_large,
        labelRow2,
        int(
            (
                displayLength
                - Writer.stringlen(wri_large, moscowTime)
                + Writer.stringlen(wri_satoshi, satoshiSymbol)
            )
            / 2
        ),
        moscowTime,
    )
    Label(
        wri_satoshi,
        labelRow2,
        int(
            (
                displayLength
                - Writer.stringlen(wri_satoshi, satoshiSymbol)
                - Writer.stringlen(wri_large, moscowTime)
            )
            / 2
        ),
        satoshiSymbol,
    )
    Label(
        wri_tiny,
        labelRow3,
        int((displayLength - Writer.stringlen(wri_tiny, mempoolFees)) / 2),
        mempoolFees,
    )
    ssd.wait_until_ready()
    refresh(ssd, False)
    ssd.wait_until_ready()
    ssd.sleep()


main()
