import sys
import os
import time
import json

import django
os.environ['DJANGO_SETTINGS_MODULE'] = 'mfpoj.settings'
django.setup()

import lorun

from contest.models import Contest, ContestProblem, ContestSubmission, ContestUser
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

def compile_cpp(waiting):
	submission = waiting.submission
	language = submission.language
	source = submission.source

	if language == "C++":
		output = open("/tmp/test.cpp", 'w')
		output.write(source)
		output.close()
		os.system("rm -rf /tmp/test;ulimit -t 5;g++ -o /tmp/test /tmp/test.cpp;ulimit -t unlimited");
		if os.path.exists("/tmp/test"):
			return True
		else:
			return False

def solve_output(f):
	with open(f,'r') as fo:
		read_in = fo.readlines()
	res = []
	for read_string in read_in:
		if read_string.endswith('\n'):
			read_string = read_string[:-1]
		read_string = read_string.rstrip()
		res.append(read_string)
	while res and res[-1] == '':
		res.pop()
	return res

def check_output(std):
	if solve_output(std) == solve_output('/tmp/output.out'):
		return 1
	else:
		return 0

def get_status_from_result(result):
	priority = {}
	for idx, status in enumerate(RESULT_STR):
		priority[status] = idx
	if len(result) == 0:
		return "System Error"
	return max([obj['result'] for obj in result])

def run_one_testcase(testcase):
	os.system("cp "+testcase.input.file.name+" /tmp/input.in")
	res=os.popen("cp /usr/bin/time /tmp/time;docker run -v /tmp:/mnt -m%dM ubuntu /bin/bash -c \"cd /mnt;ulimit -t %d; date +\'startoifajdsnvcmewrlk %%s%%N\'; { ./time -f \'memoryeiurojlkfdsjorewlkmfnaowrtoinalkdsf %%M\' ./test <input.in >output.out; } 2>&1; date +\'endnvajdfsdoifamfeie %%s%%N\'\""%((testcase.memory_limit+100)*1024,testcase.time_limit+1)).readlines() 
	rst={
		'result':'','timeused':-1,'memoryused':-1
	}
	starttime=0
	endtime=-1
	for lin in res:
		lst=lin.split()
		if lst[0]=='memoryeiurojlkfdsjorewlkmfnaowrtoinalkdsf':
			rst['memoryused']=int(lst[1])
		if lst[0]=='startoifajdsnvcmewrlk':
			starttime=int(lst[1])
		if lst[0]=='endnvajdfsdoifamfeie':
			endtime=int(lst[1])
			rst['timeused']=(endtime-starttime)/1000000
	if rst['memoryused']>testcase.memory_limit*1024:
		rst['result']='Memory Limit Exceeded'
	elif rst['timeused']>testcase.time_limit*1000:
		rst['result']='Time Limit Exceeded'
	elif len(res)!=3:
		rst['result']='Runtime Error'
	else:
		if check_output(testcase.output.file.name)==1:
			rst['result']='Accepted'
		else:
			rst['result']='Wrong Answer'
	return rst

def run_testcases(waiting):
	submission = waiting.submission
	language = submission.language

	result = []
	command = ""
	
	if language == "C++":
		testcases = len(submission.problem.testcase_set.all())
		ac = 0
		for testcase in submission.problem.testcase_set.all():	
			rst = run_one_testcase(testcase)
			if rst['result'] == 'Accepted' :
				ac += 1
			result.append(rst)
	
	submission.status = get_status_from_result(result)
	if len(result) == 0:
		submission.score = 0
	else:
		submission.score = int(round(100.0*ac/testcases))
	
	s = User.objects.filter(username = submission.user.username)[0]
	
	if submission.from_contest != 0:
		contest = Contest.objects.get(pk=submission.from_contest)
		contestuser = contest.contestuser_set.all().filter(user=s)[0]
		contest_problem = contest.contestproblem_set.filter(number=submission.from_contest_problem)[0]
		contest_obj = json.loads(contestuser.stat)
		contest_obj[contest_problem.number] = submission.score
		contestuser.stat = json.dumps(contest_obj)
		contestuser.save()
	else:
		obj = json.loads(s.stat)
		obj[submission.status] += 1
		s.stat = json.dumps(obj)
		s.save()
	
	if submission.status == 'Accepted':
		if submission.from_contest != 0:
			submission.score = 100
			contest_problem = contest.contestproblem_set.filter(number=submission.from_contest_problem)[0]
			contest_problem.ac += 1
			contest_problem.save()
		else:
			submission.score = 100
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
	submission.score = 0
	submission.save()

while True:
	waiting_list = Waiting.objects.all()
	if waiting_list:
		for waiting in waiting_list:
			s = waiting.submission.user
			if compile_cpp(waiting):
				run_testcases(waiting)
			else:
				solve_CE()
				obj = json.loads(s.stat)
				obj["Compile Error"] += 1
				s.stat = json.dumps(obj)
				s.save()
			waiting.delete()
	else:
		time.sleep(1)
