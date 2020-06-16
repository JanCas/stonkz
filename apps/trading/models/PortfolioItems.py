from django.db import models

from apps.base.models.Tickers import Tickers
from apps.trading.models.Portfolio import Portfolio


class PortfolioItems(models.Model):
    # TRANSACTION_STATUS_CHOICES = []

    portfolio = models.ForeignKey(Portfolio, on_delete=models.SET_NULL, null=True, blank=False)
    ticker = models.ForeignKey(Tickers, on_delete=models.SET_NULL, null=True, blank=False)
    shares = models.IntegerField(default=0, null=True, blank=False)
    portfolio_allocation = models.FloatField(default=1 / 3, null=True)

    def __str__(self):
        return self.ticker.symbol
