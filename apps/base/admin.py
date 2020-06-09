from django.contrib import admin
from apps.base.models.Company import Company
from apps.base.models.Ticker import Ticker

# Register your models here.
class CompanyAdmin(admin.ModelAdmin):
    list_display = ('name', 'ticker_name', 'industry')
admin.site.register(Company, CompanyAdmin)


class TickerAdmin(admin.ModelAdmin):
    list_display = ('symbol', 'closing_price', 'market_cap', 'outstanding_shares', 'exchange')
admin.site.register(Ticker, TickerAdmin)