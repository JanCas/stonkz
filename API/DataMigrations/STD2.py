import django
import os
import sys
import random

BASE_PATH = os.path.dirname('../stonkz/')
sys.path.append(BASE_PATH)
os.environ['DJANGO_SETTING_MODULE'] = 'stonkz.settings'
django.setup()


def generate_portfolio(name, cash=10000, strategy='ADOSC', positions=3):
    import numpy as np
    from apps.base.models.Tickers import Tickers
    from apps.trading.models.PortfolioItems import PortfolioItems

    print('creating Portfolio')
    portfolio = create_portfolio(strategy=strategy, positions=positions, name=name, cash=cash)
    print('portfolio Created')

    tickers = np.array(list(Tickers.objects.all()))
    ticker_indeces = random.sample(range(len(tickers)), positions)

    print('creating items')
    for ticker in tickers[ticker_indeces]:
        kwargs = {
            'portfolio': portfolio,
            'portfolio_allocation': 1 / positions,
            'ticker': ticker
        }
        PortfolioItems.objects.get_or_create(**kwargs)


def create_portfolio(strategy, positions, name, cash):
    from apps.trading.models.TradingStrategy import TradingStrategy
    from apps.trading.models.Portfolio import Portfolio

    trading_strat = TradingStrategy.objects.get_or_create(**{'strategy': strategy})[0]

    kwargs = {
        'trading_strategy': trading_strat,
        'positions': positions,
        'name': name,
        'cash': cash,
        'value': cash,
    }
    portfolio = Portfolio.objects.get_or_create(**kwargs)[0]
    return portfolio


generate_portfolio(name='trial')
