from math import pi, sin
from color_setup import ssd
from gui.core.writer import Writer
from gui.core.nanogui import refresh

import time


def main():
    refresh(ssd, True)
    ssd.wait_until_ready()
    time.sleep(80)
    print("clear")
    ssd.sleep()
    print("sleep")


main()
