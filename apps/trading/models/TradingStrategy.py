from django.db import models
from apps.base.models.Control import Control



class TradingStrategy(Control):
    ADOSC = 0
    MOVING_AVERAGES = 1
    TRADING_STRAT_CHOICES = [
        (ADOSC, 'ADOSC'),
        (MOVING_AVERAGES, 'Moving Averages')
    ]

    strategy = models.CharField(max_length=10,
                                default=None,
                                choices=TRADING_STRAT_CHOICES,
                                null=False)

    class Meta:
        verbose_name_plural = 'Trading Strategies'
        verbose_name = 'Trading Strategy'

    def MovingAverage(self, ticker, buy_volume):
        from yahooquery import Ticker
        import talib
        import alpaca_trade_api as trade
        from stonkz.settings import ALPACA_API_KEY, ALPACA_API_SECRET, APCA_API_BASE_URL

        alpaca = trade.REST(ALPACA_API_KEY, ALPACA_API_SECRET, APCA_API_BASE_URL, api_version='v2')

    #retrieve ticker
        yahoo_ticker = Ticker(ticker)
    #get prices from ticker
        prices = yahoo_ticker.history()
    #calculate simple moving average
        sma = talib.SMA(prices['close'], timeperiod=20)

    #if the price goes from below the sma to above, buy
        if prices['close'][-2] < sma[-2] and prices['close'][-1] > sma[-1]:
            alpaca.submit_order(ticker, buy_volume, 'buy', 'market', 'day')

    #if the price goes from above the sma to below, short
        elif prices['close'][-2] > sma[-2] and prices['close'][-1] < sma[-1]:
            alpaca.submit_order(ticker, buy_volume, 'short', 'market', 'day')




    def ADOSC(self, ticker, stay_below_zero, buy_volume, threshold_diffrence=2):
        from yahooquery import Ticker
        import talib
        import alpaca_trade_api as trade
        from stonkz.settings import ALPACA_API_KEY, ALPACA_API_SECRET, APCA_API_BASE_URL

        alpaca = trade.REST(ALPACA_API_KEY, ALPACA_API_SECRET, APCA_API_BASE_URL, api_version='v2')

        yahoo_ticker = Ticker(ticker)
        history = yahoo_ticker.history()
        ticker_adosc = talib.ADOSC(high=history['high'], low=history['low'], close=history['close'],
                                   volume=history['volume'])
        ticker_adosc_pct = ticker_adosc.pct_change()

        if ticker_adosc_pct[-2] < 0 and \
                abs(ticker_adosc_pct[-2] - ticker_adosc_pct[-1]) > threshold_diffrence and \
                ticker_adosc_pct[-1] > 0:
            alpaca.submit_order(ticker, buy_volume, 'buy', 'market', 'day')
