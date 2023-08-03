import orangeClockFunctions.displayBlockMoscowFees as orangeClock
from wifi import wifimgr  # importing the Wi-Fi manager library
from time import sleep
import machine
import gc

try:
    import usocket as socket
except:
    import socket
#machine.reset() #reset pi
led = machine.Pin("LED", machine.Pin.OUT)
wlan = wifimgr.get_connection()  # initializing wlan
if wlan is None:
    print("Could not initialize the network connection.")
    while True:
        pass
print("wifi-manager connected")

orangeClock.setSecrets(list(wifimgr.read_profiles().keys())[0], wifimgr.read_profiles()[list(wifimgr.read_profiles().keys())[0]])
orangeClock.main()
