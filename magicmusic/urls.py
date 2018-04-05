from django.conf.urls import include, url
from django.contrib.auth import views as auth_views
from magicmusic import views

urlpatterns = [
    url(r'^$', views.mymusic, name='mymusic'),
    # url(r'^profile', views.profile, name='profile'),
    # url(r'^follower', views.follower, name='follower'),
    url(r'^addsong', views.addsong, name='addsong'),
    url(r'^workspace/(?P<id>\d+)$', views.workspace, name='workspace'),
    url(r'^track/(?P<id>\d+)$', views.track, name='track'),
]