from django.contrib import admin

from .models.Portfolio import Portfolio
from .models.PortfolioItems import PortfolioItems
from .models.TradingStrategy import TradingStrategy
from .models.TradingStrategyItems import TradingStrategyItem
from .models.TradeHistoryItem import TradeHistoryItem


# Register your models here.
class PortfolioItemInline(admin.TabularInline):
    model = PortfolioItems
    ordering = ('-used_in_momentum',)


class TradingStrategyItemInline(admin.TabularInline):
    model = TradingStrategyItem


class TradeHistoryItemInline(admin.TabularInline):
    model = TradeHistoryItem


class PortfolioAdmin(admin.ModelAdmin):
    inlines = [PortfolioItemInline,
               TradingStrategyItemInline,
               TradeHistoryItemInline]
    list_display = ('name', 'value', 'pct_change', 'trading_strategy', 'positions')
    actions = ['run_trade',
               'get_value',
               'set_name']

    def run_trade(self, request, queryset):
        for x in queryset:
            x.run()

    def get_value(self, request, queryset):
        for x in queryset:
            x.get_value()

    def set_name(self, request, queryset):
        for x in queryset:
            x.set_name()


admin.site.register(Portfolio, PortfolioAdmin)
admin.site.register(TradingStrategy)
