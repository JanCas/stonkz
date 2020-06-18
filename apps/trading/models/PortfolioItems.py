from django.db import models

from apps.base.models.Tickers import Tickers
from apps.trading.models.Portfolio import Portfolio


class PortfolioItems(models.Model):
    HOLD = 0
    SHORT = 1
    TRANSACTION_STATUS_CHOICES = [
        (HOLD, 'Holding'),
        (SHORT, 'Shorting')
    ]

    portfolio = models.ForeignKey(Portfolio, on_delete=models.SET_NULL, null=True, blank=False)
    ticker = models.ForeignKey(Tickers, on_delete=models.SET_NULL, null=True, blank=False)
    shares = models.IntegerField(default=0, null=True, blank=False)
    portfolio_allocation = models.FloatField(default=None, null=True)
    transaction_status = models.SmallIntegerField(default=None, choices=TRANSACTION_STATUS_CHOICES, blank=True, null=True)
    value = models.FloatField(default=None, blank=True, null=True)
    cash_allocated = models.FloatField(default=None, blank=True, null=True)

    def __str__(self):
        return self.ticker.symbol

    def set_value(self):
        self.ticker.update_closing_price()
        self.value = self.shares * self.ticker.previous_closing_price
        self.save()
