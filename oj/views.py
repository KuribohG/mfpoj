from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect

from .models import Problem, Submission, Waiting, User

def index(request):
    if('username' in request.session.keys()):
        context = {'len': len(request.session['username']), 'name': request.session['username']}
    else:
        context = {'len': 0, 'name': ''}
    return render(request, 'index.html',context)
   # return HttpResponse("欢迎来到魔法炮OJ！")

def problemset(request):
    problem_list = Problem.objects.all()
    if('username' in request.session.keys()):
        context = {'problem_list': problem_list,'len': len(request.session['username']), 'name': request.session['username']}
    else:
        context = {'problem_list': problem_list,'len': 0, 'name': ''}
    return render(request, 'problemset.html', context)

def problem(request, problem_id):
    problem = Problem.objects.get(pk=problem_id)
    if('username' in request.session.keys()):
        context = {'problem': problem,'len': len(request.session['username']), 'name': request.session['username']}
    else:
        context = {'problem': problem,'len': 0, 'name': ''}
    return render(request, 'problem.html', context)

def submit(request, **kwargs):
    if request.method == 'POST':
        if 'username' in request.session.keys():
            submission = Submission(
                             problem=Problem.objects.get(pk=request.POST['problem_id']),
                             source=request.POST['source'],
                             language=request.POST['language'],
                             user=User.objects.filter(username=request.session['username'])[0], 
                             status="Pending", 
                         )
            submission.save()
            waiting=Waiting(submission=submission)
            waiting.save()
        else:
            return HttpResponse("You should login first.")
    if 'problem_id' in kwargs.keys():
        problem = Problem.objects.get(pk=kwargs['problem_id'])
    else:
        problem = None
    if('username' in request.session.keys()):
        context = {'problem': problem,'len': len(request.session['username']), 'name': request.session['username']}
    else:
        context = {'problem': problem,'len': 0, 'name': ''}
    return render(request, 'submit.html', context)

def login(request):
    error_message = ""
    if request.method == 'POST':
        if len(request.POST['username']) == 0:
            error_message = "Empty username."
        elif len(request.POST['password']) == 0:
            error_message = "Empty password."
        else:
            s = User.objects.filter(username=request.POST['username'])
            if len(s) == 0 or request.POST['password'] != s[0].password:
                error_message = "Incorrect username or password."
            else:
                request.session['username'] = request.POST['username']
                return HttpResponseRedirect('/')
    if('username' in request.session.keys()):
        context = {'error_message': error_message,'len': len(request.session['username']), 'name': request.session['username']}
    else:
        context = {'error_message': error_message,'len': 0, 'name': ''}
    return render(request, 'login.html', context)

def register(request):
    error_message = ""
    if request.method == 'POST':
        if request.POST['password'] != request.POST['password2']:
            error_message = "Passwords mismatched."
        elif len(request.POST["username"]) == 0:
            error_message = "Empty username."
        elif len(request.POST["username"]) > 15:
            error_message = "Username too long."
        elif len(request.POST["password"]) == 0:
            error_message = "Empty password."
        elif len(request.POST["password"]) > 20:
            error_message = "Password too long."
        elif len(User.objects.filter(username=request.POST['username'])):
            error_message = "This username has been registered."
        else:
            user = User(username=request.POST['username'], password=request.POST['password'],nickname=request.POST['username'])
            user.save()
    if('username' in request.session.keys()):
        context = {'error_message': error_message,'len': len(request.session['username']), 'name': request.session['username']}
    else:
        context = {'error_message': error_message,'len': 0, 'name': ''}
    return render(request, 'register.html', context)

def logout(request):
    del request.session['username']
    return HttpResponseRedirect('/')

def ranklist(request):
    user_list = User.objects.all()
    if('username' in request.session.keys()):
        context = {'user_list':user_list,'len': len(request.session['username']), 'name': request.session['username']}
    else:
        context = {'user_list':user_list,'len': 0, 'name': ''}
    return render(request, 'ranklist.html',context)

def status(request):
    submission_list = Submission.objects.all()
    submission_list = list(submission_list)[-50:]
    submission_list.reverse()
    if('username' in request.session.keys()):
        context = {'submission_list': submission_list,'len': len(request.session['username']), 'name': request.session['username']}
    else:
        context = {'submission_list': submission_list,'len': 0, 'name': ''}
    return render(request, 'status.html',context)

def modify(request):
    error_message = ""
    if request.method == 'POST':
        if len(request.POST['opassword']) == 0:
            error_message = "Please input old password."
        else:
            s = User.objects.filter(username=request.session['username'])[0]
            if  request.POST['opassword'] != s.password:
                error_message = "Incorrect old password."
            elif request.POST['password'] != request.POST['password2']:
                error_message = "Passwords mismatched."
            elif len(request.POST["password"]) > 20:
                error_message = "Password too long."
            elif len(request.POST["password"]) == 0:
                s.nickname=request.POST['nickname']
                s.save()
            else:
                s.nickname=request.POST['nickname']
                s.save()
    if('username' in request.session.keys()):
        context = {'error_message': error_message,'len': len(request.session['username']), 'name': request.session['username']}
    else:
        return HttpResponse("You should login first.")
    return render(request, 'modify.html',context)

