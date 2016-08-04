import sys
import os
import time

import django
os.environ['DJANGO_SETTINGS_MODULE'] = 'mfpoj.settings'
django.setup()

from oj.models import Waiting

def judge(waiting):
    submission = waiting.submission
    language = submission.language
    source = submission.source

    if language == "C++":
        output = open("/tmp/test.cpp", 'w')
        output.write(source)
        output.close()
        os.system("g++ -o /tmp/test /tmp/test.cpp")
        os.system("/tmp/test")

while True:
    waiting_list = Waiting.objects.all()

    if waiting_list:
        for waiting in waiting_list:
            judge(waiting)
            waiting.delete()
    else:
        time.sleep(1)
