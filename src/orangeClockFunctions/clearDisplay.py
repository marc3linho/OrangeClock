from math import pi, sin
from color_setup import ssd
from gui.core.writer import Writer
from gui.core.nanogui import refresh

import gui.fonts.freesans70 as large
import time

wri_large = Writer(ssd, large, verbose=False)
wri_large.set_clip(False, False, False)

def main():
    refresh(ssd, True)
    ssd.wait_until_ready()
    time.sleep(80)
    print("clear")
    ssd.sleep()
    print("sleep")
    
main()