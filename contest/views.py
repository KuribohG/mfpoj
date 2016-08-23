from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect

from .models import Contest, ContestProblem, ContestSubmission
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

def contest(request, contest_id):
    return HttpResponse("OK")

def submit(request, contest_id, problem_id):
    pass
