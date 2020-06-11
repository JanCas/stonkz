from django.db import models

from apps.base.models.Control import Control
from apps.base.models.Ticker import Ticker


class Company(Control):
    name = models.CharField(max_length=100, default=None, null=False)
    description = models.TextField(help_text='description of company', null=True)
    ticker_name = models.ForeignKey(Ticker, on_delete=models.CASCADE, null=True, blank=True, verbose_name='ticker')
    beta = models.FloatField(default=0, null=True)
    industry = models.CharField(max_length=20, default=None, null=True)
    equity_valuation = models.FloatField(default=-1, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Company'
        verbose_name_plural = 'Companies'

    def calculate_DCF(self):
        print('calculating DCF for {}'.format(name))
        ticker = self.ticker_name
        sum = 0
        cash_flow = ticker.free_cash_flow
        for year in range(1, ticker.years_for_valuation+1):
            cash_flow *= (1 + ticker.growth_rate)
            sum += cash_flow / ((1+ticker.discount_rate) ** year)
        sum += (ticker.pe_ratio * ticker.net_income_to_common) / ((1+ticker.discount_rate) ** year)

        self.equity_valuation = sum
        self.save()
