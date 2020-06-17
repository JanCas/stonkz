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
    prices = test_ticker.history()
    sma = talib.SMA(prices['close'], timeperiod=20)

    for x in range(3, prices['close'].size):
        if prices['close'][x-2] < sma[x-2] and prices['close'][x-1] > sma[x-1]:
            print("bought at " + str(prices['close'][x]))
        elif prices['close'][x-2] > sma[x-2] and prices['close'][x-1] < sma[x-1]:
            print("sold short at " + str(prices['close'][x]))
