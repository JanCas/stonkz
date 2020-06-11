from django.contrib import admin
from apps.base.models.Company import Company
from apps.base.models.Ticker import Ticker


class CompanyAdmin(admin.ModelAdmin):
    list_display = ('name', 'ticker_name', 'industry')
    actions = ['calculate_DCF']

    def calculate_DCF(self, request, queryset):
        pass
admin.site.register(Company, CompanyAdmin)


class TickerAdmin(admin.ModelAdmin):
    list_display = ('symbol', 'previous_closing_price', 'market_cap', 'outstanding_shares', 'exchange')
admin.site.register(Ticker, TickerAdmin)