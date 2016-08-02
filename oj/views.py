from django.shortcuts import render
from django.http import HttpResponse

from .models import Problem

def index(request):
    return HttpResponse("It works.")

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
