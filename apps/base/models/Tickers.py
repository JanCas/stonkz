from django.db import models


class Tickers(models.Model):
    symbol = models.CharField(max_length= 20, default=None, null=False)
    previous_closing_price = models.FloatField(default=None, null=True)
    price_now = models.FloatField(default=None, null=True)
    market_cap = models.FloatField(default=None, null=True)
    free_cash_flow = models.FloatField(default=None, null=True)
    pe_ratio = models.FloatField(default=None, null=True)
    discount_rate = models.FloatField(default=.02, null=True)
    net_income_to_common = models.FloatField(default=None, null=True)
    growth_rate = models.FloatField(default=None, null=True)

    outstanding_shares = models.IntegerField(default=None, null=True)
    exchange = models.CharField(max_length=10, default='NYSC', null=True)
    currency = models.CharField(max_length=10, default='USD')

    years_for_valuation = models.IntegerField(default=5, null=True, help_text='set the years for the company valuation')

    class Meta:
        verbose_name_plural = 'Tickers'
        verbose_name = 'Ticker'
        ordering = ['symbol']

    def __str__(self):
        return self.symbol

    def update_closing_price(self):
        from yahooquery import Ticker

        ticker = Ticker(self.symbol)
        self.previous_closing_price = ticker.summary_detail[self.symbol]['previousClose']
        self.save()

    def update_price(self):
        from yahooquery import Ticker

        ticker = Ticker(self.symbol)
        self.price_now = ticker.financial_data[self.symbol]['currentPrice']
        self.save()