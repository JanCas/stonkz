from django.db import models
from apps.base.models.Control import Control


class TradingStrategy(Control):
    ADOSC = 'ADOSC'
    MOVING_AVERAGES = 'MOVING AVERAGES'
    VOLUME_PRESSURE = 'VOLUME PRESSURE'
    TRADING_STRAT_CHOICES = [
        (ADOSC, 'ADOSC'),
        (MOVING_AVERAGES, 'Moving Averages'),
        (VOLUME_PRESSURE, 'Volume Pressure')
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


def adosc(transaction_volume, portfolio_item, buy_threshold_difference=2, sell_threshold_difference=2, period='5d',
          fastperiod=3, slowperiod=10):
    """
    strategy that trades based on reversals in the chaikin oscillator
    :param transaction_volume:
    :param portfolio_item:
    :param buy_threshold_difference:
    :param sell_threshold_difference:
    :param period:
    :param fasperiod:
    :param slowperiod:
    :return:
    """
    from yahooquery import Ticker
    import talib
    import alpaca_trade_api as trade
    from .TradeHistoryItem import log_trade
    from stonkz.settings import ALPACA_API_KEY, ALPACA_API_SECRET, APCA_API_BASE_URL
    from API.Help import pct_change

    alpaca = trade.REST(ALPACA_API_KEY, ALPACA_API_SECRET, APCA_API_BASE_URL, api_version='v2')
    ticker = str(portfolio_item)
    yahoo_ticker = Ticker(ticker)
    history = yahoo_ticker.history(period=period, interval=portfolio_item.portfolio.get_trading_frequency())
    ticker_adosc = talib.ADOSC(high=history['high'], low=history['low'], close=history['close'],
                               volume=history['volume'], fastperiod=fastperiod, slowperiod=slowperiod)
    ticker_adosc_pct = pct_change(ticker_adosc)

    # Buy when in the bottom of a dip in the chalking oscillator graph
    if ticker_adosc_pct[-2] < 0 and \
            abs(ticker_adosc_pct[-2] - ticker_adosc_pct[-1]) > buy_threshold_difference and \
            ticker_adosc_pct[-1] > 0:
        if portfolio_item.transaction_status == 2:  # only buy to cover if stock has been shorted before
            print('buying to cover {} shares of {}'.format(transaction_volume, ticker))
            alpaca.submit_order(ticker, transaction_volume, 'buy', 'market', 'day')
            log_trade(portfolio_item=portfolio_item, transaction_volume=transaction_volume, transaction_type=2)
        print('buying {} shares of {}'.format(transaction_volume, ticker))
        alpaca.submit_order(ticker, transaction_volume, 'buy', 'market', 'day')
        portfolio_item.buy(transaction_volume=transaction_volume)
        log_trade(portfolio_item=portfolio_item, transaction_volume=transaction_volume, transaction_type=0)

    # Sell at a tip in chaikin oscillator
    elif ticker_adosc_pct[-2] > 0 and \
            abs(ticker_adosc_pct[-2] - ticker_adosc_pct[-1]) > sell_threshold_difference and \
            ticker_adosc_pct[-1] < 0:
        if portfolio_item.transaction_status == 0:  # making sure stock exists before selling it
            print('selling {} shares of {}'.format(transaction_volume, ticker))
            alpaca.submit_order(ticker, transaction_volume, 'sell', 'market', 'day')
            portfolio_item.sell(transaction_volume=transaction_volume)
            log_trade(portfolio_item=portfolio_item, transaction_volume=transaction_volume, transaction_type=1)
        if portfolio_item.transaction_status != 2:  # make sure we dont short twice in a row
            print('shorting {} shares of {}'.format(transaction_volume, ticker))
            alpaca.submit_order(ticker, transaction_volume, 'sell', 'market', 'day')
            portfolio_item.short(transaction_volume=transaction_volume)
            log_trade(portfolio_item=portfolio_item, transaction_volume=transaction_volume, transaction_type=3)
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


def vol_pressure(portfolio_item, transaction_volume, long=27, short=3, period='5d'):
    from yahooquery import Ticker
    import talib
    import alpaca_trade_api as trade
    from .TradeHistoryItem import log_trade
    from stonkz.settings import ALPACA_API_KEY, ALPACA_API_SECRET, APCA_API_BASE_URL

    alpaca = trade.REST(ALPACA_API_KEY, ALPACA_API_SECRET, APCA_API_BASE_URL, api_version='v2')

    yahoo_ticker = Ticker(str(portfolio_item))
    prices = yahoo_ticker.history(period=period, interval=portfolio_item.portfolio.get_trading_frequency())

    volume = prices['volume']
    volume_normalized = volume / talib.EMA(volume, timeperiod=long)
    balance_of_power = talib.BOP(prices['open'], prices['high'], prices['low'], prices['close'])
    buy_pressure = balance_of_power[balance_of_power > 0]
    sell_pressure = balance_of_power[balance_of_power < 0]
    buy_pressure_normalized = ((buy_pressure / talib.EMA(buy_pressure, timeperiod=long)) * volume_normalized) * 100
    sell_pressure_normalized = ((sell_pressure / talib.EMA(sell_pressure, timeperiod=long)) * volume_normalized) * 100
    total_pressure_normalized = buy_pressure + sell_pressure
    nbf = talib.EMA(talib.EMA(buy_pressure_normalized, timeperiod=short), timeperiod=short)
    nsf = talib.EMA(talib.EMA(sell_pressure_normalized, timeperiod=short), timeperiod=short)
    tpf = talib.EMA(talib.EMA(total_pressure_normalized, timeperiod=short), timeperiod=short)
    vpo2 = ((sum(nbf, long) - sum(nsf, long)) / sum(tpf, long)) * 100

    if vpo2[-2] < 0 and vpo2[-1] > 0:
        print('buying {} shares of {}'.format(transaction_volume, str(portfolio_item)))
        alpaca.submit_order(str(portfolio_item), transaction_volume, 'buy', 'market', 'day')
        log_trade(portfolio_item=portfolio_item, transaction_volume=transaction_volume, transaction_type=0)
    elif vpo2[-2] > 0 and vpo2[-1] < 0 and portfolio_item.transaction_status == 0:
        print('buying {} shares of {}'.format(transaction_volume, str(portfolio_item)))
        alpaca.submit_order(str(portfolio_item), transaction_volume, 'sell', 'market', 'day')
        log_trade(portfolio_item=portfolio_item, transaction_volume=transaction_volume, transaction_type=1)
