from django.contrib import admin
from apps.base.models.Company import Company
from apps.base.models.Tickers import Tickers


class CompanyAdmin(admin.ModelAdmin):
    list_display = ('name', 'ticker_name', 'industry', 'equity_valuation', 'calculated_share_price', 'pct_change', 'beta')
    actions = ['calculate_DCF']

    def calculate_DCF(self, request, queryset):
        for x in queryset:
            x.calculate_dcf()
admin.site.register(Company, CompanyAdmin)


class TickerAdmin(admin.ModelAdmin):
    list_display = ('symbol', 'previous_closing_price', 'market_cap', 'outstanding_shares', 'exchange')
    actions = ['update_closing_price',
               'update_price']
    search_fields = ['symbol']

    def update_closing_price(self, request, queryset):
        for x in queryset:
            x.update_closing_price()

    def update_price(self, request, queryset):
        for x in queryset:
            x.update_price()
admin.site.register(Tickers, TickerAdmin)