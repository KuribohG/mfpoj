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

    error_message = ""
    if request.method == 'POST':
        if not "problem_id" in request.POST.keys():
            return HttpResponse("Please tell me the problem ID.")
        if logined:
            contest = Contest.objects.get(pk=contest_id)
            if time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()+3600*8))<contest.start.strftime('%Y-%m-%d %H:%M:%S'):
                return HttpResponse("Contest not started!")
            elif time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()+3600*8))>contest.end.strftime('%Y-%m-%d %H:%M:%S'):
                return HttpResponse("Contest ended!")
            else:
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
                                 from_contest=contest_id,	
                                 from_contest_problem=problem_id,	
                                 contest_start_time=contest.start,
                                 contest_end_time=contest.end,
                                 length=len(request.POST['source']),
                                 submit_time=time.strftime('%Y-%m-%d %X', time.localtime(time.time()+3600*8)),
                                 time_used=0, 
                                 memory_used=0, 
                                 contest=contest, 
                                 contest_problem=contest_problem,
                                 contest_user=contestuser,
                             )
                submission.save()

                contest_obj = json.loads(contestuser.stat)
                if problem_id in contest_obj.keys():
                    pass
                else:
                    contest_obj[problem_id] = 0
                    contestuser.stat = json.dumps(contest_obj)
                    contestuser.save()
                
                contest_problem.submit += 1
                contest_problem.save()
    
                waiting=Waiting(submission=submission.submission_ptr)
                waiting.save()
                return HttpResponseRedirect('/contest/'+str(contest_id)+'/status')

    contest = Contest.objects.get(pk=contest_id)
    context = {
        'error_message': error_message,
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
    
    for contest_user in contest.contestuser_set.all():
        contest_user.score = 0
        for problem in problem_list:
            contest_obj = json.loads(contest_user.stat)
            if problem.number in contest_obj:
                contest_user.score += contest_obj[problem.number]
        contest_user.save()
    
    nowtime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()+3600*8))
    
    if(logined):
        join = 0
        user = User.objects.filter(username=request.session['username'])[0]
        for contest_user in contest.contestuser_set.all():
            if contest_user.user == user:
                join = 1
        if join == 1:
            contestuser = contest.contestuser_set.all().filter(user=user)[0]
            obj = json.loads(contestuser.stat)
            context = {
                'nowtime': nowtime,
                'stat': obj,
                'join': 1,
                'contest': contest, 
                'problem_list': problem_list, 
                'logined': 1,
                'name': request.session['username'], 
                'page_name': 'contest',
            }
        else:
            context = {
                'nowtime': nowtime,
                'join': 0,
                'contest': contest, 
                'problem_list': problem_list, 
                'logined': 1,
                'name': request.session['username'], 
                'page_name': 'contest',
            }
    else:
        context = {
            'nowtime': nowtime,
            'contest': contest, 
            'problem_list': problem_list, 
            'logined': 0,
            'name': '', 
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
    nowtime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()+3600*8))
    
    context = {
        'nowtime': nowtime,
        'contest': contest, 
        'contest_id': contest_id, 
        'submission_list': submission_list, 
        'logined': int(logined),  
        'name': request.session['username'] if logined else '',
        'page_name': 'status',
    }
    return render(request, 'contest_status.html',context)
def contest_standings(request, contest_id):
    
    contest = Contest.objects.get(pk=contest_id)
    problem_list = contest.contestproblem_set.all()
    
    for contest_user in contest.contestuser_set.all():
        contest_user.score = 0
        for problem in problem_list:
            contest_obj = json.loads(contest_user.stat)
            if problem.number in contest_obj:
                contest_user.score += contest_obj[problem.number]
        contest_user.save()
        
    user_list = contest.contestuser_set.order_by("-score","user")
    user_list = list(user_list)
        
    #分页大法开启
    users_per_page = 50
    paginator = Paginator(user_list, users_per_page)
    if 'page' in request.GET.keys():
        nowpage = request.GET['page']
    else:
        nowpage = 1
    try:
        user_list = paginator.page(nowpage) 
    except PageNotAnInteger:
        user_list = paginator.page(1)
    except EmptyPage:
        user_list = paginator.page(paginator.num_pages)
    #分页大法结束
    
    logined = 'username' in request.session.keys()
    nowtime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()+3600*8))
    
    context = {
        'nowtime': nowtime,
        'contest': contest, 
        'contest_id': contest_id, 
        'user_list': user_list, 
        'problem_list': problem_list,
        'logined': int(logined),  
        'name': request.session['username'] if logined else '',
        'page_name': 'standings',
    }
    return render(request, 'contest_standings.html',context)

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

