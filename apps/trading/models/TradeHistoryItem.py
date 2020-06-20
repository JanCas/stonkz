from django.db import models
from django.utils import timezone


class TradeHistoryItem(models.Model):
    BUY = 0
    SELL = 1
    BUY_TO_COVER = 2
    SHORT = 3
    TRANSACTION_TYPE_CHOICES = [
        (BUY, 'buy'),
        (SELL, 'sell'),
        (BUY_TO_COVER, 'buy to cover'),
        (SHORT, 'short')
    ]

    portfolio = models.ForeignKey('trading.Portfolio', on_delete=models.CASCADE, null=False)
    ticker = models.ForeignKey('base.Tickers', on_delete=models.CASCADE, null=False)
    time_filed = models.DateTimeField(default=timezone.now)
    transaction_volume = models.IntegerField(default=None, null=False)
    transaction_type = models.SmallIntegerField(default=0, choices=TRANSACTION_TYPE_CHOICES, null=False)

    class Meta:
        verbose_name = 'Transaction'
        verbose_name_plural = 'Transactions'


def log_trade(portfolio_item, transaction_volume, transaction_type):
    kwargs = {
        'portfolio': portfolio_item.portfolio,
        'ticker': portfolio_item.ticker,
        'transaction_volume': transaction_volume,
        'trasaction_type': transaction_type
    }
    TradeHistoryItem.objects.create(**kwargs)
