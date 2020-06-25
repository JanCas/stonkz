from django.db import models

from apps.base.models.Control import Control


class ModelTraining(Control):
    REGRESSION = 0
    CLASSIFICATION = 1
    MODEL_TYPE_CHOICES = [
        (REGRESSION, 'regression'),
        (CLASSIFICATION, 'classification')
    ]

    sklearn_model = models.CharField(max_length=50, default=None, null=False)
    ticker = models.ForeignKey('base.Tickers', on_delete=models.CASCADE, null=False)
    portfolio = models.ForeignKey('trading.Portfolio', on_delete=models.SET_NULL, null=True, blank=True)
    accuracy = models.IntegerField(default=None, null=True, blank=True)
    model_type = models.SmallIntegerField(default=CLASSIFICATION, choices=MODEL_TYPE_CHOICES, null=False)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Model Training'
