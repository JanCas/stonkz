import django
import os
import sys

BASE_PATH = os.path.dirname('../stonkz/')
sys.path.append(BASE_PATH)
os.environ['DJANGO_SETTING_MODULE'] = 'stonkz.settings'
django.setup()

def generate_portfolio(strategy='ADOSC'):
    pass

def create_portfolio():
    from apps.trading.models.TradingStrategy import TradingStrategy

    trading_strat = TradingStrategy.objects.get_or_create(**{})