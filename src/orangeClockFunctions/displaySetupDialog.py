from color_setup import ssd
from gui.core.nanogui import refresh
from orangeClockFunctions.compositors import composeSetup

import time
setupTxt = "Setup:" 
wifiTxt = "OrangeClockWifi"  
URITxt = "URI: orange.clock" 

def main():
    refresh(ssd, True)
    ssd.wait_until_ready()

    composeSetup(
        ssd,
        (setupTxt, "J"),
        (wifiTxt, "L"),
        (URITxt, "D")
    )

    refresh(ssd, False)
    ssd.wait_until_ready()
    ssd.sleep()
    print("sleep")

