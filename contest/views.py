from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect

from .models import Contest, ContestProblem, ContestSubmission, ContestUser
from oj.models import User, Waiting, Submission
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
        'logined': 1 if logined else 0, 
        'name': request.session['username'] if logined else '', 
    }

    return render(request, 'contests.html', context)

def contest_submit(request, **kwargs):
    logined = 'username' in request.session.keys()
    has_problem = 'problem_id' in kwargs
    if not logined:
        return HttpResponse("You should log in first.")
    
    contest_id = int(kwargs['contest_id'])
    problem_id_letter = kwargs['problem_id'] if has_problem else 'A'
    problem_id = ord(problem_id_letter) - ord('A')
    contest = Contest.objects.get(pk=contest_id)
    contest_problem = contest.contestproblem_set.all()[problem_id]

    if request.method == 'POST':
        if not request.POST['problem_id']:
            return HttpResponse("Please tell me the problem ID.")
        if logined:
            user = User.objects.filter(username=request.session['username'])[0]
            contest = Contest.objects.get(pk=contest_id)
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
                             time_used=0, 
                             memory_used=0, 
                             contest=contest, 
                             contest_problem=contest_problem,
                             contest_user=contestuser,  
                         )
            submission.save()
            waiting=Waiting(submission=submission.submission_ptr)
            waiting.save()
        return HttpResponseRedirect('/contest/'+str(contest_id)+'/status')

    context = {
        'contest_id': contest_id, 
        'problem_id': problem_id_letter, 
        'logined': 1, 
        'name': request.session['username'], 
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
    }

    return render(request, 'contest.html', context)
