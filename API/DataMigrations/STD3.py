import django
import os
import sys

BASE_PATH = os.path.dirname('../stonkz/')
sys.path.append(BASE_PATH)
os.environ['DJANGO_SETTINGS_MODULE'] = 'stonkz.settings'
django.setup()



def create_portfolio(name, strategy, positions, cash):
    from apps.trading.models.TradingStrategy import TradingStrategy
    from apps.trading.models.Portfolio import Portfolio

    trading_strat = TradingStrategy.objects.get_or_create(**{'strategy': strategy})[0]

    kwargs = {
        'name':name,
        'trading_strategy': trading_strat,
        'positions': positions,
        'starting_cash': cash,
    }
    portfolio = Portfolio.objects.get_or_create(**kwargs)[0]
    return portfolio