from django.db import models

from apps.base.models.Tickers import Tickers
from apps.trading.models.Portfolio import Portfolio


class PortfolioItems(models.Model):
    HOLD = 0
    SOLD = 1
    SHORT = 2
    TRANSACTION_STATUS_CHOICES = [
        (HOLD, 'Holding'),
        (SOLD, 'sold'),
        (SHORT, 'Shorting')
    ]

    portfolio = models.ForeignKey(Portfolio, on_delete=models.SET_NULL, null=True, blank=False)
    ticker = models.ForeignKey(Tickers, on_delete=models.SET_NULL, null=True, blank=False)
    shares = models.IntegerField(default=0, null=True, blank=False)
    portfolio_allocation = models.FloatField(default=None, null=True)
    transaction_status = models.SmallIntegerField(default=None, choices=TRANSACTION_STATUS_CHOICES, blank=True, null=True)
    total_value = models.FloatField(default=None, blank=True, null=True)
    stock_value = models.FloatField(default=None, blank=True, null=True)
    cash_allocated = models.FloatField(default=None, blank=True, null=True)

    def __str__(self):
        return self.ticker.symbol

    def set_value(self):
        self.ticker.update_closing_price()
        self.stock_value = self.shares * self.ticker.previous_closing_price
        self.total_value = self.stock_value + self.cash_allocated
        self.save()
        return self.total_value

    def buy(self, transaction_volume):
        self.ticker.update_closing_price()
        self.shares += transaction_volume
        self.transaction_status = self.HOLD
        self.stock_value = self.shares * self.ticker.previous_closing_price
        self.cash_allocated -= self.stock_value
        self.save()

    def sell(self, transaction_volume):
        self.ticker.update_closing_price()
        self.cash_allocated += transaction_volume * self.ticker.previous_closing_price
        self.shares -= transaction_volume
        self.transaction_status = self.SOLD
        self.stock_value = self.shares * self.ticker.previous_closing_price
        self.save()