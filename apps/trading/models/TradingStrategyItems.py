from django.db import models


class TradingStrategyItem(models.Model):
    INT = 0
    STRING = 1
    FLOAT = 2
    DATA_TYPE_CHOICES = [
        (INT, 'int'),
        (STRING, 'string'),
        (FLOAT, 'float'),
    ]

    portfolio = models.ForeignKey('trading.Portfolio', on_delete=models.CASCADE, null=False)
    parameter = models.CharField(max_length=40, default=None, null=False)
    data_type = models.SmallIntegerField(default=0, choices=DATA_TYPE_CHOICES, null=True, blank=True)
    value = models.CharField(max_length=20, default=None, null=True)

    def get_value(self):
        if self.data_type == self.INT:
            return int(self.value)
        elif self.data_type == self.STRING:
            return self.value
        elif self.data_type == self.FLOAT:
            return float(self.value)
