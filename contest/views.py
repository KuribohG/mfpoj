import time
import json


from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect

from .models import Contest, ContestProblem, ContestSubmission, ContestUser
from oj.models import User, Waiting, Submission, Problem
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

def paginate(object_list, objects_per_page, now_page):
    paginator = Paginator(object_list, objects_per_page)

    try:
        object_list = paginator.page(now_page)
    except PageNotAnInteger: 
        object_list = paginator.page(1)
    except EmptyPage: 
        object_list = paginator.page(paginator.num_pages)

    return object_list

def contests(request):
    contest_list = Contest.objects.all()

    logined = 'username' in request.session.keys()
    nowpage = request.GET['page'] if 'page' in request.GET.keys() else 1
    context = {
        'contest_list': paginate(contest_list, 10, nowpage), 
        'logined': int(logined), 
        'name': request.session['username'] if logined else '', 
    }

    return render(request, 'contests.html', context)

def contest_submit(request, **kwargs):
    logined = 'username' in request.session.keys()
    if not logined:
        return HttpResponse("You should log in first.")
    
    contest_id = int(kwargs['contest_id'])
    problem_id_letter = kwargs.get('problem_id')
    if problem_id_letter is None:
        problem_id_letter = 'A'

    if request.method == 'POST':
        if not "problem_id" in request.POST.keys():
            return HttpResponse("Please tell me the problem ID.")
        if logined:
            contest = Contest.objects.get(pk=contest_id)
            problem_id = request.POST["problem_id"]
            contest_problem = contest.contestproblem_set.filter(number=problem_id)[0]
            user = User.objects.filter(username=request.session['username'])[0]
            registered = user.contestuser_set.filter(contest=contest).exists()
            if not registered:
                contestuser = ContestUser(
                                  user=user, 
                                  contest=contest, 
                              )
                contestuser.save()
            contestuser = contest.contestuser_set.all().filter(user=user)[0]
            submission = ContestSubmission(
                             problem=contest_problem.problem, 
                             source=request.POST['source'], 
                             language=request.POST['language'], 
                             user=user, 
                             status='Pending', 
                             length=len(request.POST['source']),
                             submit_time=time.strftime('%Y-%m-%d %X', time.localtime(time.time()+3600*8)),
                             time_used=0, 
                             memory_used=0, 
                             contest=contest, 
                             contest_problem=contest_problem,
                             contest_user=contestuser,  
                         )
            submission.save()

            p = contest_problem.problem
            obj = json.loads(user.stat)
            if '%d'%p.id in obj.keys():
                pass
            else:
                obj['%d'%p.id] = 0
                user.stat = json.dumps(obj)
                user.save()

            waiting=Waiting(submission=submission.submission_ptr)
            waiting.save()
        return HttpResponseRedirect('/contest/'+str(contest_id)+'/status')

    contest = Contest.objects.get(pk=contest_id)
    context = {
        'contest': contest, 
        'contest_id': contest_id, 
        'problem_id_letter': problem_id_letter, 
        'logined': 1, 
        'name': request.session['username'], 
        'page_name': 'submit',
    }
    return render(request, 'contest_submit.html', context)

def contest(request, contest_id):
    logined = 'username' in request.session.keys()
    contest = Contest.objects.get(pk=contest_id)
    problem_list = contest.contestproblem_set.all()
    
    context = {
        'contest': contest, 
        'problem_list': problem_list, 
        'logined': int(logined), 
        'name': request.session['username'] if logined else '', 
        'page_name': 'contest',
    }

    return render(request, 'contest.html', context)
    
def contest_status(request, contest_id):
    contest = Contest.objects.get(pk=contest_id)
    submission_list = contest.contestsubmission_set.all()
    submission_list = list(submission_list)
    submission_list.reverse()
    
    #分页大法开启
    submissions_per_page = 10
    paginator = Paginator(submission_list, submissions_per_page)
    if 'page' in request.GET.keys():
        nowpage = request.GET['page']
    else:
        nowpage = 1
    try:
        submission_list = paginator.page(nowpage) 
    except PageNotAnInteger:
        submission_list = paginator.page(1)
    except EmptyPage:
        submission_list = paginator.page(paginator.num_pages)
    #分页大法结束
    
    logined = 'username' in request.session.keys()
    
    context = {
        'contest': contest, 
        'contest_id': contest_id, 
        'submission_list': submission_list, 
        'logined': int(logined),  
        'name': request.session['username'] if logined else '',
        'page_name': 'status',
    }
    return render(request, 'contest_status.html',context)

def contest_problem(request, contest_id, problem_id):
    logined = 'username' in request.session.keys()
    contest = Contest.objects.get(pk=contest_id)
    contest_problem = contest.contestproblem_set.filter(number=problem_id)[0]
    real_id = contest_problem.problem.id
    problem = Problem.objects.get(pk=real_id)

    context = {
        'contest': contest, 
        'problem_id_letter':problem_id,
        'contest_id': contest_id, 
        'problem': problem,
        'logined': int(logined),  
        'name': request.session['username'] if logined else '',
        'page_name': 'problem',
    }
    return render(request, 'contest_problem.html', context)
    
def code(request, submission_id):
    submission = Submission.objects.get(pk=submission_id)
    if('username' in request.session.keys()):
        context = {'submission': submission,'logined': 1, 'name': request.session['username']}
    else:
        context = {'submission': submission,'logined': 0, 'name': ''}
    return render(request, 'code.html', context)

