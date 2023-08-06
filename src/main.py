import orangeClockFunctions.displayBlockMoscowFees as orangeClock
from wifi import wifimgr  # importing the Wi-Fi manager library
import time
import machine
import gc
import urequests
import socket

#machine.reset() #reset pi
wlan = wifimgr.get_connection()  # init
if wlan is None:
    print("Could not initialize the network connection.")
    while True:
        pass
print("wifi-manager connected")
try: ## checks if socket is open
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(('', 80))
    s.listen(5)
    time.sleep(1)

except OSError:
    print("reset in main")
    time.sleep(1)
    machine.reset()
    
if wlan_sta.isconnected():    
    orangeClock.setWifiInstance(wlan)
    orangeClock.setSecrets(str(list(wifimgr.read_profiles().keys())[0]), str(wifimgr.read_profiles()[list(wifimgr.read_profiles().keys())[0]]))
    orangeClock.main()
else:
    time.sleep(60)
    machine.reset()