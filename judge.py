import sys
import os
import time
import json

import django
os.environ['DJANGO_SETTINGS_MODULE'] = 'mfpoj.settings'
django.setup()

import lorun

from oj.models import Problem, Submission, Waiting, User

RESULT_STR = [
    'Accepted',
    'Presentation Error',
    'Time Limit Exceeded',
    'Memory Limit Exceeded',
    'Wrong Answer',
    'Runtime Error',
    'Output Limit Exceeded',
    'Compile Error',
    'System Error', 
]

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
    priority = {}
    for idx, status in enumerate(RESULT_STR):
        priority[status] = idx
    if len(result) == 0:
        return "Accepted"
    return max([obj['result'] for obj in result])

def run_one_testcase(testcase, command):
    fd_in = open(testcase.input.file.name, 'r')
    fd_out = open("/tmp/test.out", 'w')

    runcfg = {
        'args': [command], 
        'fd_in': fd_in.fileno(), 
        'fd_out': fd_out.fileno(), 
        'timelimit': testcase.time_limit,
        'memorylimit': testcase.memory_limit * 1024,
    }

    rst = lorun.run(runcfg)

    fd_in.close()
    fd_out.close()

    rst['result'] = RESULT_STR[rst['result']]
    if rst['result'] == 'Accepted':
        fd_in = open(testcase.output.file.name, 'r')
        fd_out = open("/tmp/test.out", 'r')
        rst['result'] = check_output(fd_in, fd_out)
        # check_rst = lorun.check(fd_in.fileno(), fd_out.fileno())
        # rst['result'] = RESULT_STR[check_rst]

    return rst

def run_testcases(waiting, exec_file):
    submission = waiting.submission
    language = submission.language

    result = []
    command = ""
    
    if language == "C++":
        for testcase in submission.problem.testcase_set.all():
            command = exec_file
            # os.system(exec_file + " < " + testcase.input.file.name + " > /tmp/test.out")
            # fstd = open(testcase.output.file.name)
            # fout = open("/tmp/test.out")
            result.append(run_one_testcase(testcase, command))

    submission.status = get_status_from_result(result)
    
    s = User.objects.filter(username = submission.user.username)[0]
    obj = json.loads(s.stat)
    obj[submission.status] += 1
    s.stat = json.dumps(obj)
    s.save()
    
    if submission.status == 'Accepted':
        p = submission.problem
        p.ac += 1
        p.save()
        problem_id = p.id
        if '%d'%problem_id in obj.keys() and obj['%d'%problem_id] == 1:
            pass
        else:
            s.ac += 1
            obj['%d'%problem_id] = 1
            s.stat = json.dumps(obj)
            s.save()
    
    if len(result) == 0:
        submission.time_used = 0
    else:
        submission.time_used = max([obj['timeused'] for obj in result])
    if len(result) == 0:
        submission.memory_used = 0
    else:
        submission.memory_used = max([obj['memoryused'] for obj in result])
    submission.save()
    
def solve_CE():
    submission = waiting.submission
    language = submission.language

    result = []
    
    if language == "C++":
        for testcase in submission.problem.testcase_set.all():
            result.append(dict(result='Compile Error'))

    submission.status = get_status_from_result(result)
    submission.save()

while True:
    waiting_list = Waiting.objects.all()

    if waiting_list:
        for waiting in waiting_list:
        
            s = waiting.submission.user
            #s.waiting -= 1
            #s.save()
            
            exec_file = judge(waiting)
            if exec_file != "Compile Error":
                run_testcases(waiting, exec_file)
            else:
                solve_CE()
                obj = json.loads(s.stat)
                obj["Compile Error"] += 1
                s.stat = json.dumps(obj)
                s.save()
            waiting.delete()
    else:
        time.sleep(1)
