from django.db import models
from apps.base.models.Control import Control

# Strategy based on Chaikin Oscillator, buy when change from negative to positive and difference greater than threshold difference
def adosc(ticker, transaction_volume, portfolio_item, threshold_difference=2):
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

    # Buy based on [-2] - [-1] greater than threshold and [-1] > 0
    # potentially try instead of having [-1] > 0 to buy, buy when difference between [-2] and [-1] is large enough
    if ticker_adosc_pct[-2] < 0 and \
            abs(ticker_adosc_pct[-2] - ticker_adosc_pct[-1]) > threshold_difference and \
            ticker_adosc_pct[-1] > 0:
        print('Filing Buy Order with Adosc method')
        portfolio_item.shares = transaction_volume
        portfolio_item.save()
        alpaca.submit_order(ticker, transaction_volume, 'buy', 'market', 'day')
    # Sell
    elif ticker_adosc_pct[-2] < 0 and \
            abs(ticker_adosc_pct[-2] - ticker_adosc_pct[-1]) > threshold_difference and \
            ticker_adosc_pct[-1] < 0:
        print('Filing sell order with Adosc method')
        portfolio_item.shares -= transaction_volume
        portfolio_item.save()
        alpaca.submit_order(ticker, transaction_volume, 'sell', 'market', 'day')
    # Add other indicators to aid this oscillator, correlation between this and aroon, fall at the same time there is
    # actually a dip
    # MFI, combined with chaikin shows good opportunity to buy


def moving_average(ticker, transaction_volume):
    from yahooquery import Ticker
    import talib
    import alpaca_trade_api as trade
    from stonkz.settings import ALPACA_API_KEY, ALPACA_API_SECRET, APCA_API_BASE_URL

    alpaca = trade.REST(ALPACA_API_KEY, ALPACA_API_SECRET, APCA_API_BASE_URL, api_version='v2')

    # retrieve ticker
    yahoo_ticker = Ticker(ticker)
    # get prices from ticker
    prices = yahoo_ticker.history()
    # calculate simple moving average
    sma = talib.SMA(prices['close'], timeperiod=20)

    # if the price goes from below the sma to above, buy
    if prices['close'][-2] < sma[-2] and prices['close'][-1] > sma[-1]:
        alpaca.submit_order(ticker, transaction_volume, 'buy', 'market', 'day')
    # if the price goes from above the sma to below, short
    elif prices['close'][-2] > sma[-2] and prices['close'][-1] < sma[-1]:
        alpaca.submit_order(ticker, transaction_volume, 'short', 'market', 'day')


class TradingStrategy(Control):
    ADOSC = 'ADOSC'
    MOVING_AVERAGES = 'MOVING AVERAGES'
    TRADING_STRAT_CHOICES = [
        (ADOSC, 'ADOSC'),
        (MOVING_AVERAGES, 'Moving Averages')
    ]

    strategy = models.CharField(max_length=20,
                                default=None,
                                choices=TRADING_STRAT_CHOICES,
                                null=False)

    method_name = models.CharField(max_length=20, default='adosc', null=False)

    class Meta:
        verbose_name_plural = 'Trading Strategies'
        verbose_name = 'Trading Strategy'

    def __str__(self):
        return self.strategy
