import json

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect

from .models import Problem, Submission, Waiting, User
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

def index(request):
    if('username' in request.session.keys()):
        context = {'logined': 1, 'name': request.session['username']}
    else:
        context = {'logined': 0, 'name': ''}
    return render(request, 'index.html',context)
   # return HttpResponse("欢迎来到魔法炮OJ！")

def problemset(request):
    problem_list = Problem.objects.all()
    
    #分页大法开启
    problems_per_page = 50 #每页多少道题
    paginator = Paginator(problem_list, problems_per_page)
    if 'page' in request.GET.keys():
        nowpage = request.GET['page']
    else:
        nowpage = 1
    try:
        problem_list = paginator.page(nowpage) 
    except PageNotAnInteger:
        problem_list = paginator.page(1)
    except EmptyPage:
        problem_list = paginator.page(paginator.num_pages)
    #分页大法结束
    
    if('username' in request.session.keys()):
        context = {'problem_list': problem_list,'logined': 1, 'name': request.session['username']}
    else:
        context = {'problem_list': problem_list,'logined': 0, 'name': ''}
    return render(request, 'problemset.html', context)

def problem(request, problem_id):
    problem = Problem.objects.get(pk=problem_id)
    if('username' in request.session.keys()):
        context = {'problem': problem,'logined': 1, 'name': request.session['username']}
    else:
        context = {'problem': problem,'logined': 0, 'name': ''}
    return render(request, 'problem.html', context)
    
def user(request, user_id):
    user = User.objects.filter(username=user_id)[0]
    if('username' in request.session.keys()):
        context = {'user': user,'logined': 1, 'name': request.session['username']}
    else:
        context = {'user': user,'logined': 0, 'name': ''}
    return render(request, 'user.html', context)
    
def code(request, submission_id):
    submission = Submission.objects.get(pk=submission_id)
    if('username' in request.session.keys()):
        context = {'submission': submission,'logined': 1, 'name': request.session['username']}
    else:
        context = {'submission': submission,'logined': 0, 'name': ''}
    return render(request, 'code.html', context)

def submit(request, **kwargs):
    if request.method == 'POST':
        if 'username' in request.session.keys():
            submission = Submission(
                             problem=Problem.objects.get(pk=request.POST['problem_id']),
                             source=request.POST['source'],
                             language=request.POST['language'],
                             user=User.objects.filter(username=request.session['username'])[0],
                             length=len(request.POST['source']),
                             status="Pending", 
                             time_used=0, 
                             memory_used=0,
                         )
            submission.save()
            waiting=Waiting(submission=submission)
            waiting.save()
            
            s = User.objects.filter(username=request.session['username'])[0]
            s.submit += 1
            #s.waiting += 1
            s.save()
            
            p = Problem.objects.get(pk=request.POST['problem_id'])
            p.submit += 1
            p.save()
            
            return HttpResponseRedirect('/status')
        else:
            return HttpResponse("You should login first.")
    if 'problem_id' in kwargs.keys():
        problem = Problem.objects.get(pk=kwargs['problem_id'])
    else:
        problem = None
    
    if('username' in request.session.keys()):
        context = {'problem': problem,'logined': 1, 'name': request.session['username']}
    else:
        context = {'problem': problem,'logined': 0, 'name': ''}
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
        context = {'error_message': error_message,'logined': 1, 'name': request.session['username']}
    else:
        context = {'error_message': error_message,'logined': 0, 'name': ''}
    return render(request, 'login.html', context)

def register(request):
    def stat_default():
        return {"Accepted": 0, 
                "Presentation Error": 0, 
                "Time Limit Exceeded": 0, 
                "Memory Limit Exceeded": 0, 
                "Wrong Answer": 0, 
                "Runtime Error": 0, 
                "Output Limit Exceeded": 0, 
                "Compile Error": 0, 
                "System Error": 0, 
               }

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
            user = User(username=request.POST['username'], 
                        password=request.POST['password'],
                        nickname=request.POST['username'], 
                        stat=json.dumps(stat_default()))
            user.submit = 0
            user.ac = 0
            user.save()
            return HttpResponseRedirect('/login')
    if('username' in request.session.keys()):
        context = {'error_message': error_message,'logined': 1, 'name': request.session['username']}
    else:
        context = {'error_message': error_message,'logined': 0, 'name': ''}
    return render(request, 'register.html', context)

def logout(request):
    del request.session['username']
    return HttpResponseRedirect('/')

def ranklist(request):
    all_user_list = User.objects.order_by("-ac","submit","username")
    user_list = User.objects.order_by("-ac","submit","username")
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
    if('username' in request.session.keys()):
        context = {'all_user_list':all_user_list,'user_list':user_list,'logined': 1, 'name': request.session['username']}
    else:
        context = {'all_user_list':all_user_list,'user_list':user_list,'logined': 0, 'name': ''}
    return render(request, 'ranklist.html',context)

def status(request):
    submission_list = Submission.objects.all()
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
    
    if('username' in request.session.keys()):
        context = {'submission_list': submission_list,'logined': 1, 'name': request.session['username']}
    else:
        context = {'submission_list': submission_list,'logined': 0, 'name': ''}
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
                s.school=request.POST['school']
                s.email=request.POST['email']
                s.save()
                return HttpResponseRedirect('/')
            else:
                s.nickname=request.POST['nickname']
                s.password=request.POST['password']
                s.school=request.POST['school']
                s.email=request.POST['email']
                s.save()
                return HttpResponseRedirect('/')
    if('username' in request.session.keys()):
        context = {'error_message': error_message,'logined': 1, 'name': request.session['username']}
    else:
        return HttpResponse("You should login first.")
    return render(request, 'modify.html',context)

