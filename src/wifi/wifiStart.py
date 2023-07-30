from wifi import wifimgr  # importing the Wi-Fi manager library
from time import sleep
import machine
import gc

try:
    import usocket as socket
except:
    import socket
# machine.reset() #reset pi
led = machine.Pin("LED", machine.Pin.OUT)
wlan = wifimgr.get_connection()  # initializing wlan
if wlan is None:
    print("Could not initialize the network connection.")
    while True:
        pass
print(" Raspberry Pi Pico W OK")
led_state = "OFF"


def web_page():
    html = (
        """<html>
    <head>
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <link rel="stylesheet" href="https://use.fontawesome.com/releases/v5.7.2/css/all.css"
         integrity="sha384-fnmOCqbTlWIlj8LyTjo7mOUStjsKC4pOpQbqyi7RrhN7udi9RwhKkMHpvLbHG9Sr" crossorigin="anonymous">
        <style>
            html {
                font-family: Arial;
                display: inline-block;
                margin: 0px auto;
                text-align: center;
            }

            .button {
                background-color: #ce1b0e;
                border: none;
                color: white;
                padding: 16px 40px;
                text-align: center;
                text-decoration: none;
                display: inline-block;
                font-size: 16px;
                margin: 4px 2px;
                cursor: pointer;
            }

            .button1 {
                background-color: #000000;
            }
        </style>
    </head>

    <body>
        <h2> Raspberry Pi Pico Web Server</h2>
        <p>LED state: <strong>"""
            + led_state
            + """</strong></p>
        <p>
            <i class="fas fa-lightbulb fa-3x" style="color:#c81919;"></i>
            <a href=\"?led_2_on\"><button class="button">LED ON</button></a>
        </p>
        <p>
            <i class="far fa-lightbulb fa-3x" style="color:#000000;"></i>
            <a href=\"?led_2_off\"><button class="button button1">LED OFF</button></a>
        </p>
    </body>
    </html>"""
    )
    return html


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(("", 80))
s.listen(5)

while True:
    try:
        if gc.mem_free() < 102000:
            gc.collect()
        conn, addr = s.accept()
        conn.settimeout(3.0)
        print("Received HTTP GET connection request from %s" % str(addr))
        request = conn.recv(1024)
        conn.settimeout(None)
        request = str(request)
        print("GET Rquest Content = %s" % request)
        led_on = request.find("/?led_2_on")
        led_off = request.find("/?led_2_off")
        if led_on == 6:
            print("LED ON -> GPIO2")
            led_state = "ON"
            led.on()
        if led_off == 6:
            print("LED OFF -> GPIO2")
            led_state = "OFF"
            led.off()
        response = web_page()
        conn.send("HTTP/1.1 200 OK\n")
        conn.send("Content-Type: text/html\n")
        conn.send("Connection: close\n\n")
        conn.sendall(response)
        conn.close()
    except OSError as e:
        conn.close()
        print("Connection closed")
