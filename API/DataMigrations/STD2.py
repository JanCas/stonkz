import django
import os
import sys

BASE_PATH = os.path.dirname('../stonkz/')
sys.path.append(BASE_PATH)
os.environ['DJANGO_SETTING_MODULE'] = 'stonkz.settings'
django.setup()

