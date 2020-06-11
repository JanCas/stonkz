from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class Control(models.Model):
    created_by = models.ForeignKey(User,
                                   on_delete=models.SET_NULL,
                                   null=True,
                                   editable=False,
                                   related_name="%(app_label)s_%(class)s_created",
                                   default=None,
                                   verbose_name='created_by')
    created_at = models.DateTimeField(default=timezone.now(),
                                      editable=False,
                                      verbose_name='created_at')
    changed_by = models.ForeignKey(User,
                                   on_delete=models.SET_NULL,
                                   null=True,
                                   editable=False,
                                   related_name="%(app_label)s_%(class)s_changed",
                                   default=None,
                                   verbose_name='changed_by')
    changed_at = models.DateTimeField(default=timezone.now(),
                                      editable=False,
                                      verbose_name='changed_at')