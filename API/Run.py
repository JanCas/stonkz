import django
import os
import sys

BASE_PATH = os.path.dirname('../stonkz/')
sys.path.append(BASE_PATH)
os.environ['DJANGO_SETTINGS_MODULE'] = 'stonkz.settings'
django.setup()


# TODO: make sure it returns the right things at the right time
def run(name=None):
    from apps.trading.models.Portfolio import Portfolio
    import sched, time

    scheduler = sched.scheduler(timefunc=time.time, delayfunc=time.sleep)

    portfolio = Portfolio.objects.get(name=name)

    def run_recursive():
        # portfolio.run()
        # portfolio.get_value()
        # TODO: REMOVE ONCE TESTED
        print('trading hours')
        scheduler.enterabs(delay=portfolio.trading_frequency, priority=1, action=run_recursive)

    scheduler.enterabs(delay=portfolio.trading_frequency, priority=1, action=run_recursive)
    scheduler.run()


def trigger_run(name=None):
    import sched, time
    from django.utils import timezone

    if name is None:
        name = sys.argv[1]

    scheduler = sched.scheduler(timefunc=time.time, delayfunc=time.sleep)

    def trigger_run_recursive():
        if timezone.now().isoweekday() in [6, 7]:
            print('Its the weekend')
        elif not is_trading_hours(time=timezone.now()):
            print('Its not trading hours')
        else:
            run()
        scheduler.enterabs(delay=60, priority=1, action=trigger_run_recursive)

    scheduler.enterabs(delay=60, priority=1, action=trigger_run_recursive)
    scheduler.run(name)

def is_trading_hours(time):
    pass