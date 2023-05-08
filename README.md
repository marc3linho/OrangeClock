# OrangeClock

<img src="https://nostr.build/i/nostr.build_c03eac661ef5d1912cfa2f339f1f0e98af5ce03d992efc4e49aa404c0fac33f5.jpg" width="50%" height="50%">

It is necessary to add an secrets.py file with your wlan credentials in the orangeClockFunctions folder with the following content:

SSID = "mySSID"

PASSWORD = "myPassword"

In main.py the displayed items of the OrangeClock can be selected (via comment out / uncomment)

## Hardware:

Raspberry Pi Pico W https://www.raspberrypi.com/products/raspberry-pi-pico/

Waveshare 2.9" eInk Display https://www.waveshare.com/wiki/Pico-ePaper-2.9

4 x screws M2,5x6 for the 3D printed case

## Preconditions:

Raspberry Pi Pico W with Micropython installed (https://www.raspberrypi.com/documentation/microcontrollers/micropython.html)

Thonny as IDE (much easier than VSCode with Pico-W-Go Extension (https://datasheets.raspberrypi.com/pico/raspberry-pi-pico-python-sdk.pdf))

All files in src must be copied to the Pico (except for layoutExample.py and clearDisplay.py, but they also do not interfere)

## Known bugs and strange effects

Bug: Screen remains white when no WIFI connection is established (will be fixed in the near future)

Strange effect: The display flickers every 12 hours (The reason is a full refresh).

Strange effect: After switching on, it takes about 5 minutes until the display shows something. The reason for this is the initialization of the eInk display and artifacts in other starting procedures. (will be fixed in the near future)

## Ressources:

https://www.raspberrypi.org/documentation/pico/getting-started/

https://github.com/waveshare/Pico_ePaper_Code

https://github.com/peterhinch/micropython-nano-gui/

https://github.com/peterhinch/micropython-font-to-py

https://projects.raspberrypi.org/en/projects/get-started-pico-w/2

## Acknowledgement:

Thank you gobrrr :-) (https://www.gobrrr.me/)
