from django.conf.urls import include, url
from django.contrib.auth import views as auth_views

from community import views

urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^profile', views.profile, name='profile'),
    url(r'^setting', views.profile_setting, name='profile_setting'),
    url(r'^following', views.following_users, name='following_users'),
    url(r'^profile-avatar/(?P<user_id>\d+)$', views.get_profile_avatar, name='profile-avatar'),
    url(r'^profile-bg/(?P<user_id>\d+)$', views.get_profile_bg, name='profile-bg'),
    url(r'^song-cover/(?P<song_id>\d+)$', views.get_song_cover, name='song_cover'),
    url(r'^song/(?P<song_id>\d+)$', views.get_song, name='song'),
    url(r'^logout$', auth_views.logout_then_login, name='logout'),
    # url(r'^workspace/(?P<id>\d+)$', views.workspace, name='workspace'),
]
