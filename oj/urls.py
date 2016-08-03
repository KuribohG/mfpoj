from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^problemset/$', views.problemset, name='problemset'), 
    url(r'^problem/(?P<problem_id>[0-9]+)/$', views.problem, name='problem'),
    url(r'^submit/(?P<problem_id>[0-9]+)/$', views.submit, name='submit'),
    url(r'^submit/$', views.submit, name='submit'),
    url(r'^submitting/$', views.submitting, name='submitting'), 
    url(r'^$', views.index, name='index'),
    url(r'^login/$', views.login, name='login'), 
    url(r'^register/$', views.register, name='register'), 
]
