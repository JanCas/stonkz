from apps.base.models.Control import Control
from django.db import models


class Ticker(Control):
    name = models.CharField(max_length= 20, default=None, null=False)
    closing_price = models.FloatField(default=None, null=True)
    leveraged_free_cash_flow = models.FloatField(default=None, null=True)
    outstanding_shares = models.IntegerField(default=None, null=True)
    exchange = models.CharField(max_length=10, default=None, null=True)

    def __str__(self):
        return self.name