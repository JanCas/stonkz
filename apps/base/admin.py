from django.contrib import admin
from apps.base.models.Company import Company
from apps.base.models.Ticker import Ticker

# Register your models here.
admin.site.register(Company)
admin.site.register(Ticker)


class ControlAdmin(admin.ModelAdmin):
    pass
