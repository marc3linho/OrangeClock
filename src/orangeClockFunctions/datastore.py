import time
import requests
from orangeClockFunctions.logging import log_exception


class ExternalData:
    def __init__(self, url, ttl=300, ignore_ssl_errors=False, json=True):
        self.url = url
        self.ttl = ttl
        self.json = json
        self.updated = None
        self.stale = None
        self.data = None
        self.ignore_ssl_errors = ignore_ssl_errors
        self.refresh()

    def __str__(self):
        return 'ExternalData("{}")'.format(self.url)

    def get_response(self):
        try:
            response = requests.get(self.url)
        except requests.exceptions.SSLError as ssl_error:
            if self.ignore_ssl_errors:
                response = requests.get(self.url, verify=False)
            else:
                raise ssl_error
        return response

    def refresh(self):
        now = time.time()
        answer = None

        if self.updated and self.updated + self.ttl > now:
            return answer

        try:
            response = self.get_response()
            if response.status_code == 200:
                if self.json:
                    data = response.json()
                else:
                    data = response.text
                self.updated = now
                self.stale = False
            else:
                print("status_code {}: requests.get({})".format(response.status_code, self.url))
                data = self.data
                self.stale = True
                answer = False
        except Exception as err:
            log_exception(err)
            print("Exception {}: requests.get({})".format(err, self.url))
            data = self.data
            self.stale = True
            answer = False
        finally:
            try: response.close()
            except Exception: pass

        if data != self.data:
            self.data = data
            answer = True

        return answer

#
# _extdata is a singleton dict holding ExternalData instances -- used internally
#
_extdata = {}


#
# functions for updating the _extdata singleton
#

def init_mempool_data(mempool_api, ignore_ssl_errors):
    _extdata.update({
        "prices": ExternalData(f"{mempool_api}/api/v1/prices", 300, ignore_ssl_errors),
        "fees": ExternalData(f"{mempool_api}/api/v1/fees/recommended", 120, ignore_ssl_errors),
        "height": ExternalData(f"{mempool_api}/api/blocks/tip/height", 180, ignore_ssl_errors, json=False)
    })


def initialize(mempool_api):
    keys = [x for x in _extdata.keys()]
    for key in keys:
        del _extdata[key]
    if not mempool_api:
        print("get info from mempool.space ...")
        init_mempool_data("https://mempool.space", False)
    else:
        print("get info from self-hosted mempool ...")
        init_mempool_data(mempool_api, True)


def set_nostr_pubkey(npub):
    _extdata['zaps'] = ExternalData("https://api.nostr.band/v0/stats/profile/"+npub, 300)

def refresh(raise_on_failure=False):
    refreshed = []
    failures = []
    for key, datum in _extdata.items():
        result = datum.refresh()
        if result == False:
            failures.append(key)
        elif result == True:
            refreshed.append(key)
        else:
            pass # no change
    if failures:
        msg = "datastore.refresh() had failures: {}".format(",".join(failures))
        if raise_on_failure:
            raise Exception(msg)
        else:
            print(msg)
    return refreshed


#
# functions for getting "raw" values from the _extdata singleton
#

def list_stale():
    return [k for k,v in _extdata.items() if v.stale]

def get_height():
    if "height" in _extdata:
        return int(_extdata["height"].data)

def get_price(key): # USD, EUR
    if "prices" in _extdata:
        return _extdata["prices"].data[key]

def get_fees_dict():
    if "fees" in _extdata:
        return _extdata["fees"].data

def get_nostr_zap_count():
    if "zaps" in _extdata:
        pubkey = [x for x in _extdata["zaps"].data['stats'].keys()][0]
        return _extdata["zaps"].data["stats"][pubkey]["zaps_received"]["count"]
