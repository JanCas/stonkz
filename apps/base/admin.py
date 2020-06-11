from django.contrib import admin
from apps.base.models.Company import Company
from apps.base.models.Ticker import Ticker


class CompanyAdmin(admin.ModelAdmin):
    list_display = ('name', 'ticker_name', 'industry')
    actions = ['calculate_dcf']

    def calculate_dcf(self, request, queryset):
        for x in queryset:
            x.calculate_dcf
admin.site.register(Company, CompanyAdmin)


class TickerAdmin(admin.ModelAdmin):
    list_display = ('symbol', 'previous_closing_price', 'market_cap', 'outstanding_shares', 'exchange')
admin.site.register(Ticker, TickerAdmin)