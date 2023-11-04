from color_setup import ssd
from gui.core.writer import Writer
from gui.core.nanogui import refresh
from gui.widgets.label import Label

import time
import gui.fonts.orangeClockIcons25 as iconsSmall
import gui.fonts.libreFranklinBold60 as large
import gui.fonts.libreFranklinSemiBold29 as small


wri_iconsSmall = Writer(ssd, iconsSmall, verbose=False)
wri_large = Writer(ssd, large, verbose=False)
wri_small = Writer(ssd, small, verbose=False)


labelRow1 = 5
labelRow2 = 46
labelRow3 = 85
labelCol = 10

displayLength = 296
displayHeight = 128
setupTxt = "Setup:" 
wifiTxt = "OrangeClockWifi"  
URITxt = "URI: orange.clock" 


def main():
    refresh(ssd, True)
    ssd.wait_until_ready()
    # time.sleep(10)
    Label(
        wri_small,
        labelRow1,
        int(labelCol + Writer.stringlen(wri_iconsSmall, "G") + 4),
        setupTxt,
    )

    Label(
        wri_iconsSmall,
        labelRow1 + 2,
        labelCol,
        "G",
    )
    
    Label(
        wri_small,
        labelRow2,
        int(labelCol + Writer.stringlen(wri_iconsSmall, "I") + 4),
        wifiTxt,
    )
    
    Label(
        wri_iconsSmall,
        labelRow2,
        labelCol,
        "I",
    )
    
    Label(
        wri_small,
        labelRow3,
        int(labelCol + Writer.stringlen(wri_iconsSmall, "D") + 4),
        URITxt,
    )
    
    Label(
        wri_iconsSmall,
        labelRow3 + 1,
        labelCol,
        "D",
    )

    ssd.wait_until_ready()
    refresh(ssd, False)
    ssd.wait_until_ready()
    ssd.sleep()
    print("sleep")

