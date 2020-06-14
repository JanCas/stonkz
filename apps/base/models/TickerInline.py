from django.db import models

from apps.base.models.Control import Control
from apps.base.models.Tickers import Tickers


class TickerInline(Control):
    ticker = models.ForeignKey(Tickers, on_delete=models.SET_NULL, null=False, blank=False)
    shares = models.IntegerField(default=0, null=False, blank=False)

    def __str__(self):
        return self.ticker