from django.db import models

from apps.base.models.Control import Control

class TradingStrategy(Control):
    VOLUME = 0
    MOVING_AVERAGES = 1
    TRADING_STRAT_CHOICES = [
        (VOLUME, 'Volume'),
        (MOVING_AVERAGES, 'Moving Averages')
    ]

    strategy = models.CharField(max_length=10,
                            default=None,
                            choices=TRADING_STRAT_CHOICES,
                            null=False)

    class Meta:
        verbose_name_plural = 'Trading Strategies'
        verbose_name = 'Trading Strategy'