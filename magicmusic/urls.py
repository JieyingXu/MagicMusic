from django.conf.urls import include, url
from django.contrib.auth import views as auth_views
from magicmusic import views

urlpatterns = [
    url(r'^$', views.mymusic, name='mymusic'),
    url(r'^addworkspace', views.addworkspace, name='addworkspace'),
    url(r'^workspace/(?P<id>\d+)$', views.workspace, name='workspace'),
    url(r'^track/(?P<id>\d+)$', views.track, name='track'),
]