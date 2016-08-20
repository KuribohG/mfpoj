from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^contest/$', views.contest, name='contest'), 
]
