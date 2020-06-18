import django
import os
import sys
import random

BASE_PATH = os.path.dirname('../stonkz/')
sys.path.append(BASE_PATH)
os.environ['DJANGO_SETTING_MODULE'] = 'stonkz.settings'
django.setup()


def generate_portfolio(cash=10000, strategy='ADOSC', positions=3):
    import numpy as np
    from apps.base.models.Tickers import Tickers
    from apps.trading.models.PortfolioItems import PortfolioItems

    print('creating Portfolio')
    portfolio = create_portfolio(strategy=strategy, positions=positions, cash=cash)
    print('portfolio Created')

    tickers = np.array(list(Tickers.objects.all()))
    ticker_indeces = random.sample(range(len(tickers)), positions)

    print('creating items')
    for ticker in tickers[ticker_indeces]:
        kwargs = {
            'portfolio': portfolio,
            'portfolio_allocation': 1 / positions,
            'ticker': ticker,
            'cash_allocated': cash / positions
        }
        PortfolioItems.objects.get_or_create(**kwargs)


def create_portfolio(strategy, positions, cash):
    from apps.trading.models.TradingStrategy import TradingStrategy
    from apps.trading.models.Portfolio import Portfolio

    trading_strat = TradingStrategy.objects.get_or_create(**{'strategy': strategy})[0]

    kwargs = {
        'trading_strategy': trading_strat,
        'positions': positions,
        'starting_cash': cash,
    }
    portfolio = Portfolio.objects.get_or_create(**kwargs)[0]
    portfolio.set_name()
    return portfolio


generate_portfolio()
