from django.db import models


class PortfolioItems(models.Model):
    BUY = 0
    SOLD = 1
    SHORT = 2
    BUY_TO_COVER = 3
    TRANSACTION_STATUS_CHOICES = [
        (BUY, 'Buy'),
        (SOLD, 'Sold'),
        (SHORT, 'Shorting'),
        (BUY_TO_COVER, 'Buy to Cover')
    ]

    portfolio = models.ForeignKey('trading.Portfolio', on_delete=models.CASCADE, null=False, blank=False)
    ticker = models.ForeignKey('base.Tickers', on_delete=models.SET_NULL, null=True, blank=False)
    shares = models.IntegerField(default=0, null=True, blank=False)
    portfolio_allocation = models.FloatField(default=None, null=True, blank=True)
    transaction_status = models.SmallIntegerField(default=None, choices=TRANSACTION_STATUS_CHOICES, blank=True, null=True)
    total_value = models.FloatField(default=None, blank=True, null=True)
    stock_value = models.FloatField(default=None, blank=True, null=True)
    cash_allocated = models.FloatField(default=None, blank=True, null=True)
    used_in_momentum = models.BooleanField(default=False, help_text='Only used by the momentum function')
    ai_model = models.ForeignKey('ai.ModelTraining', default=None, on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        verbose_name_plural = 'Portfolio Items'

    def __str__(self):
        return self.ticker.symbol

    def set_value(self, alpaca):
        self.ticker.update_price()
        self.stock_value = alpaca.get_position(str(self.ticker)).unrealized_pl
        if self.transaction_status == self.SHORT:
            self.total_value = self.cash_allocated
        else:
            self.total_value = self.stock_value + self.cash_allocated
        self.save()
        return self.total_value

    def buy(self, transaction_volume, cash_allocated=None):
        self.ticker.update_price()
        self.shares += transaction_volume
        self.transaction_status = self.BUY
        if str(self.portfolio.trading_strategy) == 'momentum':
            self.portfolio.update_cash_available(cash_available=cash_allocated, sign=-1)
            self.cash_allocated = cash_allocated
            self.used_in_momentum = True
        self.stock_value = self.shares * self.ticker.price_now
        self.cash_allocated -= self.stock_value
        self.save()

    def sell(self, transaction_volume):
        self.ticker.update_price()
        self.cash_allocated += transaction_volume * self.ticker.price_now
        self.shares -= transaction_volume
        self.transaction_status = self.SOLD
        self.stock_value = self.shares * self.ticker.price_now
        if str(self.portfolio.trading_strategy) == 'momentum':
            self.portfolio.update_cash_available(cash_available=self.cash_allocated, sign=1)
            self.used_in_momentum = False
            self.cash_allocated = None
        self.save()

    def short(self, transaction_volume, cash_allocated=None):
        self.ticker.update_price()
        self.transaction_status = self.SHORT
        self.stock_value = None
        self.shares -= transaction_volume
        if str(self.portfolio.trading_strategy) == 'momentum':
            self.portfolio.update_cash_available(cash_available=cash_allocated, sign=-1)
            self.cash_allocated = cash_allocated
            self.used_in_momentum = True
        self.save()

    def buy_to_cover(self, transaction_volume):
        self.ticker.update_closing_price()
        self.transaction_status = self.BUY_TO_COVER
        self.shares += transaction_volume
        self.stock_value = None
        if str(self.portfolio.trading_strategy) == 'momentum':
            self.portfolio.update_cash_available(cash_available=self.cash_allocated, sign=1)
            self.used_in_momentum = False
            self.cash_allocated = None
        self.save()
