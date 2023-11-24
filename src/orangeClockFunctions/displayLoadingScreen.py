from gui.widgets.label import Label
from gui.core.writer import Writer
from gui.core.nanogui import refresh
from color_setup import ssd

import gui.fonts.libreFranklinSemiBold29 as Small
import gui.fonts.orangeClockIcons25 as iconsSmall

wri_small = Writer(ssd, Small, verbose=False)  # Small writing
wri_iconsSmall = Writer(ssd, iconsSmall, verbose=False)  # Small icons

rowMaxDisplay = 296
labelRow1 = 5
labelRow2 = 46
labelRow3 = 85
labelCol = 10


def main(ip: str):
    """The main function for displaying a wait screen as OrangeClock loads. It also displays the connected IP address,
    so it can be seen if connection is actually successful.

    :param ip: The IP address that orange clock is connected at
    :type ip: str
    """
    txt_connected = ip
    txt_please_wait1 = "Please wait while"
    txt_please_wait2 = "OrangeClock loads..."

    refresh(ssd, True)
    ssd.wait_until_ready()
    print("Loading screen...")
    # == Row 1 ==
    # Text
    Label(
        wri_small,
        labelRow1,
        int(labelCol + Writer.stringlen(wri_iconsSmall, "I") + 4),
        txt_connected,
    )

    # Wifi icon
    Label(
        wri_iconsSmall,
        labelRow1,
        labelCol,
        "I",
    )

    # == Row 2 ==
    # Text
    Label(
        wri_small,
        labelRow2,
        labelCol,
        txt_please_wait1,
    )

    # == Row 3 ==
    # Text
    Label(
        wri_small,
        labelRow3,
        labelCol,
        txt_please_wait2,
    )

    ssd.wait_until_ready()
    refresh(ssd, False)
    ssd.wait_until_ready()
    print("sleep")
    print("Load end")
