from math import pi, sin
from color_setup import ssd
from gui.core.writer import Writer
from gui.core.nanogui import refresh
from gui.widgets.label import Label

import gui.fonts.freesans70 as large
import gui.fonts.freesans20 as small
import gui.fonts.freesans15 as tiny

wri_large = Writer(ssd, large, verbose=False)
wri_large.set_clip(False, False, False)
wri_small = Writer(ssd, small, verbose=False)
wri_small.set_clip(False, False, False)
wri_tiny = Writer(ssd, tiny, verbose=False)
wri_tiny.set_clip(False, False, False)

labelRow1 = 5
labelCol1 = 75
labelRow2 = 30
labelCol2 = 45
labelRow3 = 110
labelCol3 = 40
# Display 296*128
displayLength = 296
displayHeight = 128
blockHeight = "Block: 788383"
moscowTime = "3376"
mempoolFees = "Fees[sat/vB] L:1179 M:1190 H:1102"


def main():
    print("Length blockHeight: " + str(Writer.stringlen(wri_large, blockHeight)))
    print("Length moscowTime: " + str(Writer.stringlen(wri_small, moscowTime)))
    print("Length mempoolFees: " + str(Writer.stringlen(wri_tiny, mempoolFees)))
    refresh(ssd, True)
    ssd.wait_until_ready()
    #     Label(wri_small, labelRow1, labelCol1, blockHeight)
    #     Label(wri_large, labelRow2, labelCol2, moscowTime)
    #     Label(wri_tiny, labelRow3, labelCol3, mempoolFees)
    Label(
        wri_small,
        labelRow1,
        int((displayLength - Writer.stringlen(wri_small, blockHeight)) / 2),
        blockHeight
    )
    Label(
        wri_large,
        labelRow2,
        int((displayLength - Writer.stringlen(wri_large, moscowTime)) / 2),
        moscowTime
    )
    Label(
        wri_tiny,
        labelRow3,
        int((displayLength - Writer.stringlen(wri_tiny, mempoolFees)) / 2),
        mempoolFees
    )
    ssd.wait_until_ready()
    refresh(ssd, False)
    ssd.wait_until_ready()
    ssd.sleep()


main()
