import sys
import os

import django
os.environ['DJANGO_SETTINGS_MODULE'] = 'mfpoj.settings'
django.setup()

from oj.models import Waiting

while True:
    waiting_list = Waiting.objects.all()
    if waiting_list:
        for waiting in waiting_list:
            waiting.delete()
