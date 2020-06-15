from django.db import models

from datetime import date

from apps.base.models.Control import Control
from apps.trading.models.Portfolio import Portfolio


class Backtesting(Control):
    portfolio = models.ForeignKey(Portfolio, on_delete=models.SET_NULL, null=False)
    start_date = models.DateField(default=date(date.today().year, 1, 1))
    end_date = models.DateField(default=date.today)
