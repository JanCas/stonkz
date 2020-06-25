from django.db import models


class Company(models.Model):
    name = models.CharField(max_length=100, default=None, null=False)
    description = models.TextField(help_text='description of company', null=True)
    ticker_name = models.ForeignKey('base.Tickers', on_delete=models.CASCADE, null=True, blank=True, verbose_name='ticker')
    beta = models.FloatField(default=0, null=True)
    industry = models.CharField(max_length=20, default=None, null=True)

    equity_valuation = models.FloatField(default=-1, null=True)
    calculated_share_price = models.FloatField(default=-1, null=True)
    pct_change = models.FloatField(default=None, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Company'
        verbose_name_plural = 'Companies'

    def calculate_dcf(self):
        print('calculating DCF for {}'.format(self.name))
        ticker = self.ticker_name
        sum = 0
        cash_flow = ticker.free_cash_flow
        for year in range(1, ticker.years_for_valuation+1):
            cash_flow *= (1 + ticker.growth_rate)
            sum += cash_flow / ((1+ticker.discount_rate) ** year)
        sum += (ticker.pe_ratio * ticker.net_income_to_common) / ((1+ticker.discount_rate) ** year)

        self.equity_valuation = sum
        self.calculated_share_price = sum / ticker.outstanding_shares
        self.pct_change = (self.calculated_share_price - ticker.previous_closing_price) / ticker.previous_closing_price * 100
        self.save()
