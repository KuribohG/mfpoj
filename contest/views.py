from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect

def contest(request):
    return HttpResponse("Contest OK!")
