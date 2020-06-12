from django.db import models

from apps.base.models.Control import Control
from apps.base.models.Tickers import Tickers

class ModelTraining(Control):

    name = models.CharField(max_length=20, defualt=None, null=True)
    sklearn_model = models.CharField(max_length=20, default=None, null=False)
    ticker = models.ForeignKey(Tickers, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Model Training'

    def set_name(self):
        self.name = self.sklearn_model.split('.')[-1]
        self.save()
    