import alpaca_trade_api as tradeapi

import logging


logging.basicConfig()
logging.getLogger().setLevel(logging.DEBUG)
requests_log = logging.getLogger("requests.packages.urllib3")
requests_log.setLevel(logging.DEBUG)
requests_log.propagate = True


API_KEY = 'PK37M1QNBEZ22Z8LAKFX'
API_SECRET = 'Eu3XW0kafhNMiSM2lbONqmXlbJtZh4w/Q3gUNsBv'
APCA_API_BASE_URL = 'https://paper-api.alpaca.markets'

class Trade:
    def __init__(self):
        self.alpaca = tradeapi.REST(API_KEY, API_SECRET, APCA_API_BASE_URL, api_version='v2')

    def set_trade(self):
        self.alpaca.submit_order('TSLA',100,'buy','market','day')


t = Trade()
t.set_trade()