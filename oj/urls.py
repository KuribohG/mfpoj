from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^problemset/$', views.problemset, name='problemset'), 
    url(r'^$', views.index, name='index'), 
]
