import django
import os
import sys
import time

BASE_PATH = os.path.dirname('../stonkz/')
sys.path.append(BASE_PATH)
os.environ['DJANGO_SETTINGS_MODULE'] = 'stonkz.settings'
django.setup()


def get_index_companies():
    import bs4 as bs
    import requests

    resp = requests.get('http://en.wikipedia.org/wiki/List_of_S%26P_500_companies')
    soup = bs.BeautifulSoup(resp.text, 'lxml')
    table = soup.find('table', {'class': 'wikitable sortable'})
    tickers = []

    for row in table.findAll('tr')[1:]:
        ticker = row.findAll('td')[0].text
        ticker = ticker.strip()
        tickers.append(ticker)
        print(ticker)
    return tickers


def populate_companies_and_stocks(ticker_list=None):
    from yahooquery import Ticker

    if ticker_list is None:
        ticker_list = get_index_companies()

    for ticker in ticker_list:
        try:
            print(ticker + '-----------------------------')
            yahoo_object = Ticker(ticker)
            ticker_object = create_ticker_object(yahoo_object=yahoo_object, ticker=ticker)
            print('ticker created')
            print('creating company')
            create_company_object(yahoo_object=yahoo_object, ticker_object=ticker_object, ticker=ticker)
            time.sleep(5)
        except:
            print('Couldnt create company with ticker {}'.format(ticker))
        print()


def create_ticker_object(yahoo_object, ticker):
    from apps.base.models.Tickers import Tickers

    print('creating ticker with symbol: {}'.format(ticker))
    kwargs = {
        'symbol': ticker,
        'previous_closing_price': yahoo_object.summary_detail[ticker]['previousClose'],
        'market_cap': yahoo_object.summary_detail[ticker]['marketCap'],
        'free_cash_flow': yahoo_object.financial_data[ticker]['freeCashflow'],
        'pe_ratio': yahoo_object.valuation_measures['PeRatio'].dropna()[-1],
        'net_income_to_common': yahoo_object.key_stats[ticker]['netIncomeToCommon'],
        'growth_rate': yahoo_object.earnings_trend[ticker]['trend'][4]['growth'],  # growth rate 5 years into the future
        'outstanding_shares': yahoo_object.key_stats[ticker]['sharesOutstanding'],
        'exchange': yahoo_object.quote_type[ticker]['exchange'],
        'currency': yahoo_object.price[ticker]['currency']
    }
    return Tickers.objects.get_or_create(**kwargs)[0]


def create_company_object(yahoo_object, ticker_object, ticker):
    from apps.base.models.Company import Company

    kwargs = {
        'name': yahoo_object.price[ticker]['longName'],
        'description': yahoo_object.summary_profile[ticker]['longBusinessSummary'],
        'ticker_name': ticker_object,
        'industry': yahoo_object.summary_profile[ticker]['industry'],
        'beta': yahoo_object.key_stats[ticker]['beta']
    }
    Company.objects.get_or_create(**kwargs)
    print('Created company: ' + kwargs['name'])


populate_companies_and_stocks()