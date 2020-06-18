from django.db import models

class TradingStrategyItems(models.Model):

    parameter = models.CharField(max_length=20, default=None, null = False)