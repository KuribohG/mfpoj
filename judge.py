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
        judge_CE = os.system("g++ -o /tmp/test /tmp/test.cpp")
        if judge_CE == 0:
            return "/tmp/test"
        else:
            return "Compile Error"
def solve_output(f):
    read_in = f.readlines()
    res = []
    f.close()
    for read_string in read_in:
        if read_string.endswith('\n'):
            read_string = read_string[:-1]
        read_string = read_string.rstrip()
        res.append(read_string)
    while res and res[-1] == '':
        res.pop()
    return res

def check_output(input1, input2):
    if solve_output(input1) == solve_output(input2):
        return "Accepted"
    else:
        return "Wrong Answer"

def get_status_from_result(result):
    priority = {
        'Wrong Answer': 2, 
        'Accepted': 1, 
        'Compile Error': 3,
    }

    return max(result, key=lambda x: priority[x])

def run_testcases(waiting, exec_file):
    submission = waiting.submission
    language = submission.language

    result = []
    
    if language == "C++":
        for testcase in submission.problem.testcase_set.all():
            os.system(exec_file + " < " + testcase.input.file.name + " > /tmp/test.out")
            fstd = open(testcase.output.file.name)
            fout = open("/tmp/test.out")
            result.append(check_output(fstd, fout))

    submission.status = get_status_from_result(result)
    submission.save()

def solve_CE():
    submission = waiting.submission
    language = submission.language

    result = []
    
    if language == "C++":
        for testcase in submission.problem.testcase_set.all():
            result.append("Compile Error")

    submission.status = get_status_from_result(result)
    submission.save()

while True:
    waiting_list = Waiting.objects.all()

    if waiting_list:
        for waiting in waiting_list:
            exec_file = judge(waiting)
            if exec_file != "Compile Error":
                run_testcases(waiting, exec_file)
            else:
                solve_CE()
            waiting.delete()
    else:
        time.sleep(1)
