from math import pi, sin
from color_setup import ssd
from gui.core.writer import Writer
from gui.core.nanogui import refresh
from gui.widgets.label import Label

import gui.fonts.freesans70 as large
import gui.fonts.freesans20 as small
import gui.fonts.freesans15 as tiny
# 296*128
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

def main():
    refresh(ssd, True)
    ssd.wait_until_ready()
    Label(wri_small, labelRow1, labelCol1, "Block: 788383")
    Label(wri_large, labelRow2, labelCol2, "3376")
    Label(wri_tiny, labelRow3, labelCol3, "Fees[sat/vB] L:1179 M:1190 H:1102")
    ssd.wait_until_ready()
    refresh(ssd, False)
    ssd.wait_until_ready()
    ssd.sleep()
    
main()
