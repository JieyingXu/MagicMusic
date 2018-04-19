from django.conf.urls import include, url
from django.contrib.auth import views as auth_views
<<<<<<< HEAD
from . import views
=======
from magicmusic import views
>>>>>>> 86c582863738b94ca3c58299fc852b4151f214da

urlpatterns = [
    url(r'^$', views.mymusic, name='mymusic'),
    url(r'^profile', views.profile, name='profile'),
    url(r'^follower', views.follower, name='follower'),
    url(r'^addworkspace', views.addworkspace, name='addworkspace'),
    url(r'^workspace/(?P<id>\d+)$', views.workspace, name='workspace'),
    url(r'^track/(?P<id>\d+)$', views.track, name='track'),
    url(r'^generate-music/$', views.generate_music, name='generate-music'),
]