import sys
import os

import django
os.environ['DJANGO_SETTINGS_MODULE'] = 'mfpoj.settings'
django.setup()

from django.db import models
from oj.models import Testcase, Problem

def add_testcase(problem_id, path, time_limit, memory_limit, prefix="", From=0, To=0, suf_in=".in", suf_out=".out", MODE="Quick"):
    os.chdir(path)
    file_list = os.listdir()
    print(file_list)
    if(MODE == "Quick"):
        Input=[]
        Output=[]
        for filename in file_list:
            if os.path.splitext(filename)[1] == suf_in:
                Input.append(filename)
            elif os.path.splitext(filename)[1] == suf_out:
                Output.append(filename)
        Input.sort()
        Output.sort()
        list_tot = len(Input)
        for i in range(0,list_tot):
            s=Testcase()
            s.problem = Problem.objects.get(id=problem_id)
            in_put=open(Input[i])
            out_put=open(Output[i])
            s.input=django.core.files.File(in_put)
            s.output=django.core.files.File(out_put)
            s.time_limit = time_limit
            s.memory_limit = memory_limit
            s.save()
        return
    for i in range(From, To+1):
        s=Testcase()
        s.problem = Problem.objects.get(id=problem_id)
        Input=open(prefix+"%d"%i+suf_in)
        Output=open(prefix+"%d"%i+suf_out)
        s.input=django.core.files.File(Input)
        s.output=django.core.files.File(Output)
        s.time_limit = time_limit
        s.memory_limit = memory_limit
        s.save()

add_testcase(problem_id=1, path="/home/xrf/Desktop/oj_test", time_limit=1, memory_limit=512, suf_in=".in", suf_out=".out")
