from django.db import models

from apps.base.models.Control import Control
from apps.base.models.Ticker import Ticker


class Company(Control):
    name = models.CharField(max_length=100, default=None, null=False)
    description = models.TextField(help_text='description of company', null=True)
    earnings_last_quarter = models.FloatField(default=0, null=True)
    ticker_name = models.ForeignKey(Ticker, on_delete=models.CASCADE, null=True, blank=True, verbose_name='ticker')
    beta = models.FloatField(default=0, null=True)
    industry = models.CharField(max_length=20, default=None, null=True)

    class Meta:
        verbose_name = 'Company'
        verbose_name_plural = 'Companies'

    def __str__(self):
        return self.name
