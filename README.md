# OrangeClock

<img src="https://nostr.build/i/nostr.build_c03eac661ef5d1912cfa2f339f1f0e98af5ce03d992efc4e49aa404c0fac33f5.jpg" width="50%" height="50%">

## Hardware:

[Raspberry Pi Pico W](https://www.raspberrypi.com/products/raspberry-pi-pico/)

2 x (1x)20 pin header for the Pico or Raspberry Pi Pico WH (H - with header assembled)

[Waveshare 2.9" eInk Display](https://www.waveshare.com/wiki/Pico-ePaper-2.9)


4 x screws M2,5x6 for the 3D printed case

## Preconditions & Guide:

1. Raspberry Pi Pico W with Micropython installed [(see guide)](https://www.raspberrypi.com/documentation/microcontrollers/micropython.html)

2. Install [Thonny](https://github.com/thonny/thonny/) as IDE 
(much easier to use for beginners than VSCode with Pico-W-Go Extension (https://datasheets.raspberrypi.com/pico/raspberry-pi-pico-python-sdk.pdf)

3. All files in src must be copied to the Pico (except for layoutExample.py and clearDisplay.py, but they also do not interfere)

<img src="https://nostr.build/i/nostr.build_87ef17f889ba7f32c0272fabd280c4f4d9da0afbd17f07c45614e4a87be144fa.jpg" width="100%" height="100%">

4. It is necessary to add an secrets.py file with your wifi credentials in the orangeClockFunctions folder with the following content:
```python
SSID = "mySSID"
PASSWORD = "myPassword"
```

5. In main.py the displayed items of the OrangeClock can be selected (via comment out / uncomment)

If you have any questions, problems or suggestions please feel free to contact me at any time via nostr: npub16cpe069rjz6pm5t42xcyhcn66f5rr04k64df3g03fk2wctlrlhsqycedcd

## Known bugs and strange effects

Bug: Screen remains white when no WIFI connection is established (will be fixed in the near future)

Bug: Screen remains white when no WIFI connection is established (will be fixed in the near future)

Bug: The display does not update after a while (will be fixed in the near future)

Strange effect: The display flickers every 12 hours (The reason is a full refresh).

Strange effect: After switching on, it takes about 5 minutes until the display shows something. The reason for this is the initialization of the eInk display and artifacts in other starting procedures. (will be fixed in the near future)

## Ressources / Links:

https://www.raspberrypi.com/documentation/microcontrollers/raspberry-pi-pico.html

https://github.com/waveshare/Pico_ePaper_Code

https://github.com/peterhinch/micropython-nano-gui/

https://github.com/peterhinch/micropython-font-to-py

https://projects.raspberrypi.org/en/projects/get-started-pico-w/2

## Acknowledgement:

Thank you [gobrrr](https://www.gobrrr.me/) for your tips on 3d printing and discussing the idea :-)

