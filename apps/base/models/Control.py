from django.db import models
from django.utils import timezone

class Control(models.Model):
    created_at = models.DateTimeField(default=timezone.now(),
                                      editable=False,
                                      verbose_name='created at')
    changed_at = models.DateTimeField(default=timezone.now(),
                                      editable=False,
                                      verbose_name='changed_at')