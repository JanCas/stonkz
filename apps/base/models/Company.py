from apps.base.models import Control
from django.db import models


class Company(Control):
    name = models.CharField(max_length=100, default=None, null=False)
    earnings_last_quarter = models.FloatField(default=0, null=True)
    exceed_expectations_last_quarter = models.BooleanField(null=True)