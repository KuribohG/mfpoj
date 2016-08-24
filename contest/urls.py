from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^contests/$', views.contests, name='contests'),
    url(r'^contest/(?P<contest_id>[0-9]+)/$', views.contest, name='contest'),  
    url(r'^contest/(?P<contest_id>[0-9]+)/submit/(?P<problem_id>[A-Z]+)/$', views.contest_submit, name='contest_submit'), 
    url(r'^contest/(?P<contest_id>[0-9]+)/problem/(?P<problem_id>[A-Z]+)/$', views.contest_problem, name='contest_problem'), 
    url(r'^contest/(?P<contest_id>[0-9]+)/status/$', views.contest_status, name='contest_status'),
]
