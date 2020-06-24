from django.db import models

from apps.base.models.Control import Control
from apps.trading.models.TradingStrategy import TradingStrategy


class Portfolio(Control):
    ONE_MINUTE = 60
    FIVE_MINUTES = 300
    FIFTEEN_MINUTES = 900
    THIRTY_MINUTES = 1800
    ONE_HOUR = 3600
    TRADING_Frequency_CHOICES = [
        (ONE_MINUTE, '1min'),
        (FIVE_MINUTES, '5min'),
        (FIFTEEN_MINUTES, '15min'),
        (THIRTY_MINUTES, '30min'),
        (ONE_HOUR, '1hr')
    ]

    name = models.CharField(max_length=100, default=None, null=True)
    trading_strategy = models.ForeignKey(TradingStrategy, on_delete=models.SET_NULL, null=True,
                                         verbose_name='Trading Strategy')
    trading_frequency = models.IntegerField(default=FIFTEEN_MINUTES, choices=TRADING_Frequency_CHOICES, null=True,
                                            blank=True)

    positions = models.IntegerField(default=3, null=False, help_text='# of companies in portfolio')
    value = models.FloatField(default=None, null=True, blank=True, help_text='value of the portfolio')
    starting_cash = models.FloatField(default=10000)
    pct_change = models.FloatField(default=None, null=True, blank=True)

    def __str__(self):
        return self.name

    def run(self):
        """
        runs the appropriate trading strategy on that portfolio
        :return:
        """
        import importlib
        from math import floor
        from .PortfolioItems import PortfolioItems
        from .TradingStrategyItems import TradingStrategyItem

        # configure the inputs for the trading algorithm
        kwargs = {}
        for input_parameter in TradingStrategyItem.objects.filter(portfolio=self):
            kwargs[input_parameter.parameter] = input_parameter.get_value()

        # run the trading strategy for each Position
        for company in PortfolioItems.objects.filter(portfolio=self):
            company.ticker.update_price()
            if company.transaction_status == company.BUY or company.transaction_status == company.SHORT:
                transaction_volume = abs(company.shares)
            else:
                transaction_volume = floor(company.cash_allocated / company.ticker.price_now)
            if transaction_volume != 0:
                kwargs['transaction_volume'] = transaction_volume
                kwargs['portfolio_item'] = company
                # get run from TradingStrategy and run it
                run_method = getattr(importlib.import_module('apps.trading.models.TradingStrategy'),
                                     self.trading_strategy.method_name)
                run_method(**kwargs)

    def liquidate(self):
        """
        liquidates all positions in the portfolio if they have 10% gain or 5% loss
        :return:
        """
        import alpaca_trade_api as trade
        from stonkz.settings import ALPACA_API_KEY, ALPACA_API_SECRET, APCA_API_BASE_URL
        from .PortfolioItems import PortfolioItems
        from .TradeHistoryItem import log_trade

        alpaca = trade.REST(ALPACA_API_KEY, ALPACA_API_SECRET, APCA_API_BASE_URL, api_version='v2')

        for company in PortfolioItems.objects.filter(portfolio=self):
            try:
                if 10 > alpaca.get_position(str(company)).unrealized_plpc < -5:
                    if company.transaction_status == company.BUY:
                        print('selling {} shares of {}'.format(company.shares, str(company)))
                        alpaca.close_position(str(company))
                        log_trade(portfolio_item=company, transaction_volume=company.shares, transaction_type=1)
                        company.sell(transaction_volume=company.shares)
                    elif company.transaction_status == company.SHORT:
                        print('Buy to Cover {} shares of {}'.format(company.shares, str(company)))
                        alpaca.close_position(str(company))
                        log_trade(portfolio_item=company, transaction_volume=company.shares, transaction_type=2)
                        company.buy_to_cover(transaction_volume=company.shares)
            except:
                print('Stock {} does not exist in alpaca'.format(str(company)))

    def set_name(self):
        from .PortfolioItems import PortfolioItems
        name = '|'
        for item in PortfolioItems.objects.filter(portfolio=self):
            name += ' ' + str(item)
        self.name = str(self.trading_strategy.strategy) + name
        self.save()

    def get_value(self):
        from .PortfolioItems import PortfolioItems

        self.value = 0
        for stock in PortfolioItems.objects.filter(portfolio=self):
            self.value += stock.set_value()

        self.pct_change = (self.value - self.starting_cash) / self.starting_cash * 100.0
        self.save()

    def get_trading_frequency(self):
        if self.trading_frequency == self.ONE_MINUTE:
            return '1m'
        elif self.trading_frequency == self.FIVE_MINUTES:
            return '5m'
        elif self.trading_frequency == self.FIFTEEN_MINUTES:
            return '15m'
        elif self.trading_frequency == self.THIRTY_MINUTES:
            return '30m'
        elif self.trading_frequency == self.ONE_HOUR:
            return '60m'
