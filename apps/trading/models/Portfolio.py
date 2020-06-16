from django.db import models

from apps.base.models.Control import Control
from apps.trading.models.TradingStrategy import TradingStrategy


class Portfolio(Control):

    SHORT_TERM_TRADING = 0
    LONG_TERM_TRADING = 1
    HOLDING_STATUS_CHOICES=[
        (SHORT_TERM_TRADING, 'short term trading'),
        (LONG_TERM_TRADING, 'long term trading')
    ]

    SCREENING_METHOD_CHOICES = [

    ]

    name = models.CharField(max_length=10, default=None, null=True)
    trading_strategy = models.ForeignKey(TradingStrategy, on_delete=models.SET_NULL, null=True,
                                         verbose_name='Trading Strategy')
    holding_period = models.CharField(max_length=10,default=None, choices= HOLDING_STATUS_CHOICES, null=True, blank=True)

    positions = models.IntegerField(default=3, null=False, help_text='# of companies in portfolio')
    value = models.FloatField(default=10000, help_text='value of the portfolio')
    cash = models.FloatField(default=10000)

    def __str__(self):
        return self.name