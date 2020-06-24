import django
import os
import sys

BASE_PATH = os.path.dirname('../stonkz/')
sys.path.append(BASE_PATH)
os.environ['DJANGO_SETTINGS_MODULE'] = 'stonkz.settings'
django.setup()


def populate_portfolio(name, cash, num_of_momentum=5):
    from random import sample
    import numpy as np
    from apps.base.models.Tickers import Tickers
    from apps.trading.models.PortfolioItems import PortfolioItems

    print('creating portfolio')
    portfolio = create_portfolio(name=name, cash=cash, num_of_momentum=num_of_momentum)
    print('portfolio created')

    tickers = np.array(list(Tickers.objects.all()))
    ticker_indeces = sample(range(len(tickers)), 100)

    print('creating items')
    for ticker in tickers[ticker_indeces]:
        kwargs = {
            'portfolio': portfolio,
            'ticker': ticker,
        }
        PortfolioItems.objects.get_or_create(**kwargs)


def create_portfolio(name, num_of_momentum, cash):
    from apps.trading.models.TradingStrategy import TradingStrategy
    from apps.trading.models.Portfolio import Portfolio

    trading_strat = TradingStrategy.objects.get_or_create(**{'strategy': 'momentum'})[0]

    kwargs = {
        'name': name,
        'trading_strategy': trading_strat,
        'num_of_momentum': num_of_momentum,
        'starting_cash': cash,
    }
    portfolio = Portfolio.objects.get_or_create(**kwargs)[0]
    return portfolio

populate_portfolio(name='trial momentum', cash=100000)