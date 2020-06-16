from django.contrib import admin

from .models.Portfolio import Portfolio
from .models.PortfolioItems import PortfolioItems
from .models.TradingStrategy import TradingStrategy


# Register your models here.
class PortfolioItemInline(admin.TabularInline):
    model = PortfolioItems


class PortfolioAdmin(admin.ModelAdmin):
    inlines = [PortfolioItemInline, ]
    actions = ['run_trade', ]

    def run_trade(self, request, queryset):
        for x in queryset:
            x.run()


admin.site.register(Portfolio, PortfolioAdmin)
admin.site.register(TradingStrategy)
