import django
import os
import sys
import sched, time
from django.utils import timezone

BASE_PATH = os.path.dirname('../stonkz/')
sys.path.append(BASE_PATH)
os.environ['DJANGO_SETTINGS_MODULE'] = 'stonkz.settings'
django.setup()


# TODO: make sure it returns the right things at the right time
def run(name=None):
    from apps.trading.models.Portfolio import Portfolio

    scheduler = sched.scheduler(timefunc=time.time, delayfunc=time.sleep)

    portfolio = Portfolio.objects.get(name=name)

    def run_recursive():
        if is_trading_hours(timezone.localtime(timezone.now())):
            print('{} is running at {} -----------------'.format(name, timezone.localtime(timezone.now())))
            portfolio.run()
            portfolio.get_value()
        else:
            print('-----------------------THE MARKET HAS CLOSED AT {}----------------------------'.format(
                timezone.localtime(timezone.now())))
            trigger_run(name=name)
        scheduler.enter(portfolio.trading_frequency, priority=1, action=run_recursive)

    scheduler.enter(portfolio.trading_frequency, priority=1, action=run_recursive)
    scheduler.run()


def trigger_run(name=None):
    if name is None:
        name = sys.argv[1]
        print('name of portfolio: {}'.format(name))

    scheduler = sched.scheduler(timefunc=time.time, delayfunc=time.sleep)

    def trigger_run_recursive():
        if not is_trading_hours(timezone.localtime(timezone.now())):
            print('Its not trading hours {}'.format(timezone.localtime(timezone.now())))
        else:
            print('-----------------------THE MARKET HAS OPENED AT {}----------------------------'.format(
                timezone.localtime(timezone.now())))
            run(name)
        scheduler.enter(60, priority=1, action=trigger_run_recursive)

    scheduler.enter(30, priority=1, action=trigger_run_recursive)
    scheduler.run(name)


def is_trading_hours(time):
    return (time.hour > 9 and time.minute > 30) and (time.hour < 16) and \
           (time.isoweekday() not in [6, 7])


trigger_run()
