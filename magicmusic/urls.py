from django.conf.urls import include, url
from django.contrib.auth import views as auth_views
import views

urlpatterns = [
    url(r'^$', views.mymusic, name='mymusic'),
    url(r'^register$', views.register, name='register'),
    url(r'^profile', views.profile, name='profile'),
    url(r'^follower', views.follower, name='follower'),
    url(r'^addsong', views.addsong, name='addsong'),
    url(r'^workspace/(?P<id>\d+)$', views.workspace, name='workspace'),
    url(r'^track/(?P<id>\d+)$', views.track, name='track'),
    # Route for built-in authentication with our own custom login page
    url(r'^login$', auth_views.login, {'template_name':'magicmusic/login.html'}, name='login'),
    # Route to logout a user and send them back to the login page
    url(r'^logout$', auth_views.logout_then_login, name='logout'),
]