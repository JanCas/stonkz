from django.db import models

from datetime import date

from apps.base.models.Control import Control


class Backtesting(Control):
    ticker = models.ForeignKey('base.Tickers', on_delete=models.SET_NULL, null=False)
    start_date = models.DateField(default=date(date.today().year, 1, 1))
    end_date = models.DateField(default=date.today)


from yahooquery import Ticker
import talib

def Backtest_MA(ticker):
    test_ticker = Ticker(ticker)
    closing_prices = test_ticker.history()
    live_prices = test_ticker.history(interval='1h')
    sma = talib.SMA(closing_prices['close'], timeperiod=140)

    for x in range(75, live_prices['close'].size):
        y = 20
        if x % 7 == 0:
            y += 1
        if live_prices['close'][x-2] < sma[y] and live_prices['close'][x-1] > sma[y]:
            print("bought at " + str(live_prices['close'][x]))
        elif live_prices['close'][x-2] > sma[y] and live_prices['close'][x-1] < sma[y]:
            print("sold short at " + str(live_prices['close'][x]))
