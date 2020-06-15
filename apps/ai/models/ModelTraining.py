from django.db import models

from apps.base.models.Control import Control
from apps.base.models.Tickers import Tickers

class ModelTraining(Control):
    LONG_TERM_PERIOD = 0
    SHORT_TERM_PERIOD = 1
    PERIOD_CHOICES = [
        (LONG_TERM_PERIOD, 'long term'),
        (SHORT_TERM_PERIOD, 'short term')
    ]

    REGRESSION = 0
    CLASSIFICATION = 1
    MODEL_TYPE_CHOICES = [
        (REGRESSION, 'regression'),
        (CLASSIFICATION, 'classification')
    ]

    name = models.CharField(max_length=10, default=None, null=True)
    sklearn_model = models.CharField(max_length=10, default=None, null=False)
    ticker = models.ForeignKey(Tickers, on_delete=models.SET_NULL, null=True, blank=True)
    model_type = models.CharField(max_length=10, default=CLASSIFICATION, choices=MODEL_TYPE_CHOICES, null=False)
    period = models.CharField(max_length=10, default=None, choices=PERIOD_CHOICES, null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Model Training'

    def set_name(self):
        self.name = self.sklearn_model.split('.')[-1]
        self.save()

