from django.shortcuts import render
from django.http import HttpResponse

from .models import Problem, Submission, Waiting, User

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
    if request.method == 'POST':
        submission = Submission(
                         problem=Problem.objects.get(pk=request.POST['problem_id']),
                         source=request.POST['source'],
                         language=request.POST['language'],
                     )
        submission.save()
        waiting=Waiting(submission=submission)
        waiting.save()
    if 'problem_id' in kwargs.keys():
        problem = Problem.objects.get(pk=kwargs['problem_id'])
    else:
        problem = None
    context = {'problem': problem}
    return render(request, 'submit.html', context)

def login(request):
    return render(request, 'login.html')

def register(request):
    error_message = ""
    if request.method == 'POST':
        if request.POST['password'] != request.POST['password2']:
            error_message = "Passwords mismatched."
        elif len(request.POST["username"]) == 0:
            error_message = "Empty username."
        elif len(request.POST["password"]) == 0:
            error_message = "Empty password."
        else:
            user = User(username=request.POST['username'], password=request.POST['password'])
            user.save()
    context = {'error_message': error_message}
    return render(request, 'register.html', context)

def ranklist(request):
    return render(request, 'ranklist.html')
