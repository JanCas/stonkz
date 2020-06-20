from django.db import models
from apps.base.models.Control import Control


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


def adosc(transaction_volume, portfolio_item, buy_threshold_difference=2, sell_threshold_difference=2):
    """
    strategy based on the chalkin oscilator
    :param transaction_volume:
    :param portfolio_item:
    :param threshold_difference:
    :return:
    """
    from yahooquery import Ticker
    import talib
    import alpaca_trade_api as trade
    from stonkz.settings import ALPACA_API_KEY, ALPACA_API_SECRET, APCA_API_BASE_URL
    from API.Help import pct_change

    alpaca = trade.REST(ALPACA_API_KEY, ALPACA_API_SECRET, APCA_API_BASE_URL, api_version='v2')

    yahoo_ticker = Ticker(str(portfolio_item))
    history = yahoo_ticker.history()
    ticker_adosc = talib.ADOSC(high=history['high'], low=history['low'], close=history['close'],
                               volume=history['volume'])
    ticker_adosc_pct = pct_change(ticker_adosc)

    # Buy when in the bottom of a dip in the chalking oscillator graph
    if ticker_adosc_pct[-2] < 0 and \
            abs(ticker_adosc_pct[-2] - ticker_adosc_pct[-1]) > buy_threshold_difference and \
            ticker_adosc_pct[-1] > 0:
        if portfolio_item.transaction_status == 2: #only buy to cover if stock has been shorted before
            print(' Filing buy to cover oder with adosc method')
            alpaca.submit_order(str(portfolio_item), transaction_volume, 'buy', 'market', 'day')
        print(' Filing Buy Order with Adosc method')
        alpaca.submit_order(str(portfolio_item), transaction_volume, 'buy', 'market', 'day')
        portfolio_item.buy(transaction_volume=transaction_volume)
    # Sell at a tip in chalkin oscillator
    elif ticker_adosc_pct[-2] > 0 and \
            abs(ticker_adosc_pct[-2] - ticker_adosc_pct[-1]) > sell_threshold_difference and \
            ticker_adosc_pct[-1] < 0:
        if portfolio_item.transaction_status == 0: #making sure stock exists before selling it
            print(' Filing sell order with Adosc method')
            alpaca.submit_order(str(portfolio_item), transaction_volume, 'sell', 'market', 'day')
            portfolio_item.sell(transaction_volume=transaction_volume)
        print(' Filing short order with Adosc method')
        alpaca.submit_order(str(portfolio_item), transaction_volume, 'sell', 'market', 'day')
        portfolio_item.short(transaction_volume=transaction_volume)
    # Add other indicators to aid this oscillator, correlation between this and aroon, fall at the same time there is
    # actually a dip
    # MFI, combined with chaikin shows good opportunity to buy


def simple_moving_average(portfolio_item, transaction_volume, timeperiod=20):
    """
    trades based on the crossing of the simple moving average and the closing price
    :param portfolio_item:
    :param transaction_volume:
    :param timeperiod:
    :return:
    """
    from yahooquery import Ticker
    import talib
    import alpaca_trade_api as trade
    from stonkz.settings import ALPACA_API_KEY, ALPACA_API_SECRET, APCA_API_BASE_URL

    alpaca = trade.REST(ALPACA_API_KEY, ALPACA_API_SECRET, APCA_API_BASE_URL, api_version='v2')

    yahoo_ticker = Ticker(str(portfolio_item))
    prices = yahoo_ticker.history()
    sma = talib.SMA(prices['close'], timeperiod=timeperiod)

    # if the price goes from below the sma to above, buy
    if prices['close'][-2] < sma[-2] and prices['close'][-1] > sma[-1]:
        alpaca.submit_order(str(portfolio_item), transaction_volume, 'buy', 'market', 'day')
    # if the price goes from above the sma to below, short
    elif prices['close'][-2] > sma[-2] and prices['close'][-1] < sma[-1]:
        alpaca.submit_order(str(portfolio_item), transaction_volume, 'short', 'market', 'day')
