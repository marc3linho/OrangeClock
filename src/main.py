import orangeClockFunctions.displayBlockMoscowFees as orangeClock
import orangeClockFunctions.displaySetupDialog as setupDialog
from orangeClockFunctions.logging import log_exception
from phew import access_point, connect_to_wifi, is_connected_to_wifi, dns, server
from phew.template import render_template
import json
import machine
import os
import uio
import usys
import utime
import _thread

AP_NAME = "OrangeClockWifi"
AP_DOMAIN = "orange.clock"
AP_TEMPLATE_PATH = "ap_templates"
APP_TEMPLATE_PATH = "app_templates"
WIFI_FILE = "wifi.json"

def machine_reset():
    utime.sleep(1)
    print("Resetting...")
    machine.reset()

def setup_mode():
    print("Entering setup mode...")
    
    setupDialog.main()
    
    def ap_index(request):
        if request.headers.get("host") != AP_DOMAIN:
            return render_template(f"{AP_TEMPLATE_PATH}/redirect.html", domain = AP_DOMAIN)

        return render_template(f"{AP_TEMPLATE_PATH}/index.html")

    def ap_configure(request):
        print("Saving wifi credentials...")
        print(request.form)
        with open(WIFI_FILE, "w") as f:
            json.dump(request.form, f)
            f.close()

        # Reboot from new thread after we have responded to the user.
        _thread.start_new_thread(machine_reset, ())
        return render_template(f"{AP_TEMPLATE_PATH}/configured.html", ssid = request.form["ssid"])
        
    def ap_catch_all(request):
        if request.headers.get("host") != AP_DOMAIN:
            return render_template(f"{AP_TEMPLATE_PATH}/redirect.html", domain = AP_DOMAIN)

        return "Not found.", 404

    server.add_route("/", handler = ap_index, methods = ["GET"])
    server.add_route("/configure", handler = ap_configure, methods = ["POST"])
    server.set_callback(ap_catch_all)

    ap = access_point(AP_NAME)
    ip = ap.ifconfig()[0]
    dns.run_catchall(ip)

def application_mode():
    print("Entering application mode.")
    orangeClock.setSecrets(wifi_credentials["ssid"], wifi_credentials["password"], wifi_credentials["mempool"])
    orangeClock.setSelectDisplay(wifi_credentials["line1"], wifi_credentials["npub"], wifi_credentials["line2"])
    orangeClock.main()

    def app_index(request):
        return render_template(f"{APP_TEMPLATE_PATH}/index.html")

    def app_toggle_led(request):
        print("toogle")
        return "OK"

    def app_catch_all(request):
        return "Not found.", 404

    server.add_route("/", handler = app_index, methods = ["GET"])
    server.add_route("/toggle", handler = app_toggle_led, methods = ["GET"])
    # Add other routes for your application...
    server.set_callback(app_catch_all)

# Figure out which mode to start up in...
try:
    os.stat(WIFI_FILE)

    # File was found, attempt to connect to wifi...
    with open(WIFI_FILE) as f:
        wifi_credentials = json.load(f)
        ip_address = connect_to_wifi(wifi_credentials["ssid"], wifi_credentials["password"])

        if not is_connected_to_wifi():
            # Bad configuration, delete the credentials file, reboot
            # into setup mode to get new credentials from the user.
            print("Bad wifi connection!")
            print(wifi_credentials)
            os.remove(WIFI_FILE)
            machine_reset()

        print(f"Connected to wifi, IP address {ip_address}")
        application_mode()

except Exception as err:
    # Either no wifi configuration file found, or something went wrong, 
    # so log exception, then go into setup mode.
    log_exception(err)
    setup_mode()
    
 
# Start the web server...
server.run()

