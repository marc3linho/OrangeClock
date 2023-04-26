from math import pi, sin
from color_setup import ssd
from gui.core.writer import Writer
from gui.core.nanogui import refresh
from gui.core.fplot import CartesianGraph, Curve
from gui.widgets.meter import Meter
from gui.widgets.label import Label
from gui.widgets.dial import Dial, Pointer

import time

# Fonts
import gui.fonts.arial_50 as large

wri_large = Writer(ssd, large, verbose=False)
wri_large.set_clip(False, False, False)

# 296*128



def main():
    refresh(ssd, True)
    ssd.wait_until_ready()
    time.sleep(80)
    print("clear")
    ssd.sleep()
    print("sleep")
main()