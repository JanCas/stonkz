from django.db import models

from datetime import date

from apps.base.models.Control import Control


class Backtesting(Control):
    ticker = models.ForeignKey('base.Tickers', on_delete=models.SET_NULL, null=False)
    start_date = models.DateField(default=date(date.today().year, 1, 1))
    end_date = models.DateField(default=date.today)

def Backtest_MA(ticker):
    from yahooquery import Ticker
    import talib

    test_ticker = Ticker(ticker)
    prices = test_ticker.history()
    sma = talib.sma(prices['close'])

    for x in prices['close']:
        # if the price goes from below the sma to above, buy
        if prices['close'][x] < sma[x] and prices['close'][x+1] > sma[x+1]:
            print("bought at " + prices['close'][x+3])
        elif prices['close'][x] > sma[x] and prices['close'][x+1] < sma[x+1]
            print("sold short at " + prices['close'][x+3])