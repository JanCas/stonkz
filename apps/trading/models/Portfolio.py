from django.db import models


class Portfolio(models.Model):
    ONE_MINUTE = 60
    TWO_MINUTES = 120
    FIVE_MINUTES = 300
    FIFTEEN_MINUTES = 900
    THIRTY_MINUTES = 1800
    ONE_HOUR = 3600
    TRADING_Frequency_CHOICES = [
        (ONE_MINUTE, '1min'),
        (TWO_MINUTES, '2min'),
        (FIVE_MINUTES, '5min'),
        (FIFTEEN_MINUTES, '15min'),
        (THIRTY_MINUTES, '30min'),
        (ONE_HOUR, '1hr')
    ]

    name = models.CharField(max_length=100, default=None, null=True)
    trading_strategy = models.ForeignKey('trading.TradingStrategy', on_delete=models.SET_NULL, null=True,
                                         verbose_name='Trading Strategy')
    trading_frequency = models.IntegerField(default=FIFTEEN_MINUTES, choices=TRADING_Frequency_CHOICES, null=True,
                                            blank=True)

    positions = models.IntegerField(default=3, null=False, help_text='# of companies in portfolio')
    value = models.FloatField(default=None, null=True, blank=True, help_text='value of the portfolio')
    starting_cash = models.FloatField(default=10000)
    cash_available = models.FloatField(default=None, null=True, blank=True, help_text='Only used for momentum')
    pct_change = models.FloatField(default=None, null=True, blank=True)
    num_of_momentum = models.IntegerField(default=None, null=True, blank=True, help_text='Only used for momentum')

    def __str__(self):
        return self.name

    def run(self):
        """
        runs the appropriate trading strategy on that portfolio
        :return:
        """
        from importlib import import_module
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
            if self.trading_strategy.strategy == 'momentum':
                momentum_active = self.get_num_of_momentum()
                if momentum_active == self.num_of_momentum:
                    print('max companies already traded')
                    break
                cash_to_item = self.cash_available / (self.num_of_momentum - momentum_active)
                transaction_volume = floor(cash_to_item / company.ticker.price_now)
                kwargs['cash_allocation'] = cash_to_item
            else:
                if company.transaction_status == company.BUY or company.transaction_status == company.SHORT:
                    transaction_volume = abs(company.shares)
                else:
                    transaction_volume = floor(company.cash_allocated / company.ticker.price_now)

            if transaction_volume != 0:
                kwargs['transaction_volume'] = transaction_volume
                kwargs['portfolio_item'] = company
                # get run from TradingStrategy and run it
                run_method = getattr(import_module('apps.trading.models.TradingStrategy'),
                                     self.trading_strategy.strategy)
                run_method(**kwargs)

    def liquidate(self):
        """
        liquidates all positions in the portfolio if they have 10% gain or 5% loss
        :return:
        """
        from API.Help import initialize_alpaca
        from .PortfolioItems import PortfolioItems
        from .TradeHistoryItem import log_trade

        alpaca = initialize_alpaca()

        for company in PortfolioItems.objects.filter(portfolio=self):
            try:
                if .1 < alpaca.get_position(str(company)).unrealized_plpc < -.05:
                    if company.transaction_status == company.BUY:
                        print('selling {} shares of {}'.format(company.shares, str(company)))
                        alpaca.close_position(str(company))
                        log_trade(portfolio_item=company, transaction_volume=company.shares, transaction_type=1)
                        company.sell(transaction_volume=company.shares)
                        company.used_in_momentum = False
                    elif company.transaction_status == company.SHORT:
                        print('Buy to Cover {} shares of {}'.format(company.shares, str(company)))
                        alpaca.close_position(str(company))
                        log_trade(portfolio_item=company, transaction_volume=company.shares, transaction_type=2)
                        company.buy_to_cover(transaction_volume=company.shares)
                        company.used_in_momentum = False
            except:
                pass

    def get_num_of_momentum(self):
        from .PortfolioItems import PortfolioItems

        count = 0
        for company in PortfolioItems.objects.filter(portfolio=self):
            if company.used_in_momentum:
                count += 1
        return count

    def set_name(self):
        from .PortfolioItems import PortfolioItems
        name = '|'
        for item in PortfolioItems.objects.filter(portfolio=self):
            name += ' ' + str(item)
        self.name = str(self.trading_strategy.strategy) + name
        self.save()

    def get_value(self):
        from .PortfolioItems import PortfolioItems
        from API.Help import initialize_alpaca

        alpaca = initialize_alpaca()

        self.value = 0
        if self.trading_strategy.strategy == 'momentum':
            if self.get_num_of_momentum() == 0:
                return
            else:
                for stock in PortfolioItems.objects.filter(portfolio=self, used_in_momentum=True):
                    self.value += stock.set_value(alpaca=alpaca)
                self.value += self.cash_available
        else:
            for stock in PortfolioItems.objects.filter(portfolio=self):
                self.value += stock.set_value(alpaca=alpaca)

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

    def get_max_period(self):
        from django.utils import timezone

        if self.trading_frequency == self.ONE_MINUTE:
            return timezone.now().date() - timezone.timedelta(days=6)
        elif self.trading_frequency == self.TWO_MINUTES or \
            self.trading_frequency == self.FIVE_MINUTES or \
            self.trading_frequency == self.FIFTEEN_MINUTES or \
            self.trading_frequency == self.THIRTY_MINUTES:
            return timezone.now().date() - timezone.timedelta(days=59)
        elif self.trading_frequency == self.ONE_HOUR:
            return timezone.now().date() - timezone.timedelta(days=729)

    def update_cash_available(self, cash_available, sign):
        self.cash_available += (cash_available * sign)
        self.save()