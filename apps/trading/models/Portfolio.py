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
    trading_frequency = models.IntegerField(default=FIFTEEN_MINUTES, null=True, blank=True)

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
        import math
        from .PortfolioItems import PortfolioItems
        from .TradingStrategyItems import TradingStrategyItem

        # configure the inputs for the trading algorithm
        kwargs = {}
        for input in TradingStrategyItem.objects.filter(portfolio=self):
            kwargs[input.parameter] = input.get_value()

        for company in PortfolioItems.objects.filter(portfolio=self):
            company.ticker.update_closing_price()

            print('{} ---------------------------------'.format(company))
            transaction_volume = math.floor(company.cash_allocated / company.ticker.previous_closing_price)
            print(' allocation dollar: {} transaction volume: {}'.format(company.cash_allocated, transaction_volume))
            kwargs['transaction_volume'] = transaction_volume
            kwargs['portfolio_item'] = company
            # get run method from TradingStrategy and run it
            run_method = getattr(importlib.import_module('apps.trading.models.TradingStrategy'),
                                 self.trading_strategy.method_name)
            run_method(**kwargs)
            print()

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
