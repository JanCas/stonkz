from django.contrib import admin

from apps.trading.models.Portfolio import Portfolio
from apps.trading.models.PortfolioItems import PortfolioItem


# Register your models here.
class PortfolioItemInline(admin.TabularInline):
    model = PortfolioItem


class PortfolioAdmin(admin.ModelAdmin):
    inlines = [PortfolioItemInline, ]


admin.site.register(Portfolio, PortfolioAdmin)
