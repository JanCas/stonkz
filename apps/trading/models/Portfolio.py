from django.db import models

from apps.base.models.Control import Control
from apps.trading.models.TradingStrategy import TradingStrategy


class Portfolio(Control):
    SHORT_TERM_TRADING = 0
    LONG_TERM_TRADING = 1
    HOLDING_STATUS_CHOICES = [
        (SHORT_TERM_TRADING, 'short term trading'),
        (LONG_TERM_TRADING, 'long term trading')
    ]


    name = models.CharField(max_length=30, default=None, null=True)
    trading_strategy = models.ForeignKey(TradingStrategy, on_delete=models.SET_NULL, null=True,
                                         verbose_name='Trading Strategy')
    holding_period = models.SmallIntegerField(default=None, choices=HOLDING_STATUS_CHOICES, null=True,
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
        import math
        from .PortfolioItems import PortfolioItems
        from .TradingStrategyItems import TradingStrategyItem

        #configure the inputs for the trading algorithm
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