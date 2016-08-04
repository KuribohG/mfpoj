import sys
import os
import time

import django
os.environ['DJANGO_SETTINGS_MODULE'] = 'mfpoj.settings'
django.setup()

from oj.models import Waiting

waiting_list = Waiting.objects.all()
if waiting_list:
    for waiting in waiting_list:
        waiting_language=waiting.submission.language
        waiting_source=waiting.submission.source
        #print(waiting_language)
        if  waiting_language == "C++" :
            #print("g++")
            #print(waiting_source)
            waiting_output=open("/tmp/test.cpp",'w')
            waiting_output.write(waiting_source)
            waiting_output.close()
            os.system("g++ -o /tmp/test /tmp/test.cpp")
            os.system("/tmp/test")
        elif waiting_language == "Python" :
            #print("Python3")
            pass
        waiting.delete()
