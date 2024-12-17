<picture>
	<source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/marc3linho/OrangeClock/90b6e2c70c04c6a3153371c7495a8f971b55a9f4/logo/dark/png/logo-dark.png">
  <img src="https://raw.githubusercontent.com/marc3linho/OrangeClock/f310ad9b1bc2dffdf91db50cc76138efc2a45393/logo/light/png/logo.png">
</picture>

<img src="https://raw.githubusercontent.com/marc3linho/OrangeClock/main/images/readme/OrangeClock_1.jpeg" width="100%">

## Hardware:

[Raspberry Pi Pico W](https://www.raspberrypi.com/products/raspberry-pi-pico/)

2 x (1x)20 pin header for the Pico or Raspberry Pi Pico WH (H - with header assembled)

* soldering is only necessary with the Pico W

[Waveshare 2.9" eInk Display (**with socket for Raspberry Pi Pico!**)](https://www.waveshare.com/pico-epaper-2.9.htm)


4 x screws M2,5x6 for the 3D printed case

## Preconditions & Guide:

1. Raspberry Pi Pico W with Micropython installed [(see guide)](https://www.raspberrypi.com/documentation/microcontrollers/micropython.html) 

	A version tested with the OrangeClock is in this repository under "firmware"

2. Install [Thonny](https://github.com/thonny/thonny/) as IDE 
(much easier to use for beginners than VSCode with Pico-W-Go Extension (https://datasheets.raspberrypi.com/pico/raspberry-pi-pico-python-sdk.pdf)

	Select the interpreter in Thonny:
	```
		Select Tools -> Options -> Interpreter
		Select MicroPython (Raspberry Pi Pico and ttyACM0 port)
	```

3. All files in src must be copied to the Pico (except for layoutExample.py and clearDisplay.py, but they also do not interfere)

<img src="https://raw.githubusercontent.com/marc3linho/OrangeClock/main/images/readme/thonny_1.png" width="100%" height="100%">

4. After restart (unplug and replug the OrangeClock) you can access the wifi-manager with your phone or computer (ssid = OrangeClockWifi) and open the URI orange.clock (http://orange.clock/) in your browser

<img src="https://raw.githubusercontent.com/marc3linho/OrangeClock/main/images/readme/wifi_1.png" width="50%" >

5. Set your wifi credentials and save them, the OrangeClock will reboot automatically and connect to your network.
If you want to use your self-hosted mempool, you can enter the url. Leave it empty to use mempool.space 

<img src="https://raw.githubusercontent.com/marc3linho/OrangeClock/main/images/readme/wifi_2.jpg" width="50%" >

6. Wait until the clock appears on the screen

If you have any questions, problems or suggestions please feel free to contact me at any time via nostr: npub16cpe069rjz6pm5t42xcyhcn66f5rr04k64df3g03fk2wctlrlhsqycedcd

## Known bugs and strange effects

* The wifi credentials are stored in plain text on the Pico, so the OrangeClock should be connected to an isolated network or guest network.
When you want to use your self-hosted mempool make sure that the url is reachable from the network

* Strange effect: The display flickers every 12 hours (The reason is a full refresh).

* Strange effect: After switching on, it takes about 2 minutes until the display shows something. The reason for this is the initialization of the eInk display and artifacts in other starting procedures. (will be fixed in the near future)

* Strange effect: After reconnecting to the WIFI network or other connection issues, the following errors are displayed: 
This also happens when one of the data sources is temporarily unavailable. The update cycle is reduced to one minute until all data is available again.
<img src="https://raw.githubusercontent.com/marc3linho/OrangeClock/main/images/readme/error_1.jpeg" width="50%" height="50%">

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

Thank you for your support and cooperation in this project

[Easy](https://github.com/easyuxd) 

[Printer_GoBrrr](https://www.gobrrr.me/) 

[SeedSigner](https://SeedSigner.com)

List of [contributors](https://github.com/marc3linho/OrangeClock/graphs/contributors)
