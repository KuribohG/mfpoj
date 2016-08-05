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
        return "/tmp/test"

def solve_output(input):
    f = open(input,'r')
    read_in = f.readlines()
    f.close()
    read_counter = 0
    for read_string in read_in :
        if read_string.endswith('\n') == True :
            read_string = read_string[:-1]
        read_string = read_string.rstrip()
        read_in[read_counter] = read_string
        read_counter += 1
    while read_in[-1] == '' :
        read_in.pop()
    return read_in

def checkAC(input1,input2):
    if solve_output(input1) == solve_output(input2) :
        return "AC"
    else :
        return "WA"

def run_testcases(waiting, exec_file):
    submission = waiting.submission
    language = submission.language
    
    if language == "C++":
        for testcase in submission.problem.testcase_set.all():
            os.system(exec_file + " < " + testcase.input.file.name + " > /tmp/test.out")
            #TODO: compare test.out and stdout, return a judge status
            return "Accepted"

while True:
    waiting_list = Waiting.objects.all()

    if waiting_list:
        for waiting in waiting_list:
            exec_file = judge(waiting)
            run_testcases(waiting, exec_file)
            waiting.delete()
    else:
        time.sleep(1)
