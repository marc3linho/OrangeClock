# OrangeClock

<img src="https://raw.githubusercontent.com/marc3linho/OrangeClock/add_Wifi_Manager/images/orangeclock.jpg" width="50%" height="50%">

## Hardware:

[Raspberry Pi Pico W](https://www.raspberrypi.com/products/raspberry-pi-pico/)

2 x (1x)20 pin header for the Pico or Raspberry Pi Pico WH (H - with header assembled)

* soldering is only necessary with the Pico W

[Waveshare 2.9" eInk Display](https://www.waveshare.com/wiki/Pico-ePaper-2.9)


4 x screws M2,5x6 for the 3D printed case

## Preconditions & Guide:

1. Raspberry Pi Pico W with Micropython installed [(see guide)](https://www.raspberrypi.com/documentation/microcontrollers/micropython.html)

2. Install [Thonny](https://github.com/thonny/thonny/) as IDE 
(much easier to use for beginners than VSCode with Pico-W-Go Extension (https://datasheets.raspberrypi.com/pico/raspberry-pi-pico-python-sdk.pdf)

	Select the interpreter in Thonny:
	```
		Select Tools -> Options -> Interpreter
		Select MicroPython (Raspberry Pi Pico and ttyACM0 port)
	```

3. All **files** in **src** must be copied to the Pico (except for layoutExample.py and clearDisplay.py, but they also do not interfere)

<img src="https://raw.githubusercontent.com/marc3linho/OrangeClock/add_Wifi_Manager/images/thonny.jpg" width="100%" height="100%">

4. After restart (unplug and replug the OrangeClock) you can access the wifi-manager with your phone or computer (ssid = pi orange) and open the URI orange.clock in your browser

<img src="https://raw.githubusercontent.com/marc3linho/OrangeClock/add_Wifi_Manager/images/wifi1.jpg" width="50%" >

5. Set your wifi credentials and save them, the OrangeClock will reboot automatically and connect to your network

<img src="https://raw.githubusercontent.com/marc3linho/OrangeClock/add_Wifi_Manager/images/wifi2.jpg" width="50%" >

6. Wait until the clock appears on the screen

If you have any questions, problems or suggestions please feel free to contact me at any time via nostr: npub16cpe069rjz6pm5t42xcyhcn66f5rr04k64df3g03fk2wctlrlhsqycedcd

## Known bugs and strange effects

Strange effect: The display flickers every 12 hours (The reason is a full refresh).

Strange effect: After switching on, it takes about 5 minutes until the display shows something. The reason for this is the initialization of the eInk display and artifacts in other starting procedures. (will be fixed in the near future)

## Ressources / Links:

https://satsymbol.com/

https://www.raspberrypi.com/documentation/microcontrollers/raspberry-pi-pico.html

https://github.com/waveshare/Pico_ePaper_Code

https://github.com/peterhinch/micropython-nano-gui/

https://github.com/peterhinch/micropython-font-to-py

https://projects.raspberrypi.org/en/projects/get-started-pico-w/2

https://microcontrollerslab.com/raspberry-pi-pico-w-wi-fi-manager-web-server/

https://github.com/tayfunulu/WiFiManager

https://github.com/cpopp/MicroPythonSamples

https://github.com/simonprickett/phewap

## Acknowledgement:

Thank you [gobrrr](https://www.gobrrr.me/) for your help on 3d printing and discussing the idea :-)
