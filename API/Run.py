import os
import sched
import sys
import time

import django
from django.utils import timezone

BASE_PATH = os.path.dirname('../stonkz/')
sys.path.append(BASE_PATH)
os.environ['DJANGO_SETTINGS_MODULE'] = 'stonkz.settings'
django.setup()


def run(name=None):
    """
    Runs while markets are open
    :param name:
    :return:
    """
    from apps.trading.models.Portfolio import Portfolio

    scheduler = sched.scheduler(timefunc=time.time, delayfunc=time.sleep)

    portfolio = Portfolio.objects.get(name=name)

    def run_recursive():
        if is_trading_hours(timezone.localtime(timezone.now())):
            print('------------------------{} is running at {} -----------------'.format(name, timezone.localtime(
                timezone.now()).time()))
            portfolio.run()
            portfolio.get_value()
            if portfolio.trading_strategy.method_name == 'simple_moving_average':
                print('--------checking for liquidation----------')
                portfolio.liquidate()
            print('waiting for next period')
            print()
        else:
            print('-----------------------THE MARKET HAS CLOSED AT {}----------------------------'.format(
                timezone.localtime(timezone.now())))
            trigger_run(name=name)
        scheduler.enter(portfolio.trading_frequency, priority=1, action=run_recursive)

    scheduler.enter(0, priority=1, action=run_recursive)
    scheduler.run()


def trigger_run(name=None):
    """
    Runs during the time that markets arent open
    Checks for markets opening each minute
    :param name:
    :return:
    """
    if name is None:
        name = sys.argv[1]
        print('name of portfolio: {}'.format(name))

    scheduler = sched.scheduler(timefunc=time.time, delayfunc=time.sleep)

    def trigger_run_recursive():
        if is_trading_hours(timezone.localtime(timezone.now())):
            print('-----------------------THE MARKET HAS OPENED AT {}----------------------------'.format(
                timezone.localtime(timezone.now())))
            print()
            run(name)
        scheduler.enter(60, priority=1, action=trigger_run_recursive)

    print('Waiting for markets to open')
    scheduler.enter(0, priority=1, action=trigger_run_recursive)
    scheduler.run(name)


def is_trading_hours(time_input):
    from datetime import time

    start_time = time(9, 30, 0)
    end_time = time(16, 0, 0)
    return start_time < time_input.time() < end_time and \
           (time_input.isoweekday() not in [6, 7])


trigger_run()