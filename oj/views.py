from django.shortcuts import render
from django.http import HttpResponse

from .models import Problem, Submission, Waiting

def index(request):
    return render(request, 'index.html')
   # return HttpResponse("欢迎来到魔法炮OJ！")

def problemset(request):
    problem_list = Problem.objects.all()
    context = {'problem_list': problem_list}
    return render(request, 'problemset.html', context)

def problem(request, problem_id):
    problem = Problem.objects.get(pk=problem_id)
    context = {'problem': problem}
    return render(request, 'problem.html', context)

def submit(request, **kwargs):
    if 'problem_id' in kwargs.keys():
        problem = Problem.objects.get(pk=kwargs['problem_id'])
    else:
        problem = None
    context = {'problem': problem}
    return render(request, 'submit.html', context)

def submitting(request):
    submission = Submission(
                     problem=Problem.objects.get(pk=request.POST['problem_id']), 
                     source=request.POST['source'], 
                 )
    submission.save()
    waiting = Waiting(submission=submission)
    waiting.save()
    return HttpResponse('Success')

def login(request):
    return render(request, 'login.html')

def register(request):
    return render(request, 'register.html')
