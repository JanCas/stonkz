from django.db import models

from apps.base.models.Control import Control
from apps.trading.models.TradingStrategy import TradingStrategy

class Portfolio(Control):
    name = models.CharField(default=None, null=False)
    trading_strategy = models.ForeignKey(TradingStrategy, on_delete=models.SET_NULL, null=False, verbose_name='Trading Strategy')

    
