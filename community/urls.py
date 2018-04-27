from django.conf.urls import include, url
from django.contrib.auth import views as auth_views

from community import views

urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^profile/(?P<profile_id>\d+)$', views.profile, name='profile'),
    url(r'^setting', views.profile_setting, name='profile-setting'),
    url(r'^following/(?P<profile_id>\d+)$', views.following_users, name='following-users'),
    # url(r'^profile-avatar/(?P<profile_id>\d+)$', views.get_profile_avatar, name='profile-avatar'),
    # url(r'^profile-bg/(?P<profile_id>\d+)$', views.get_profile_bg, name='profile-bg'),
    # url(r'^song-cover/(?P<song_id>\d+)$', views.get_song_cover, name='song-cover'),
    url(r'^song/(?P<song_id>\d+)$', views.get_song, name='song'),
    # url(r'^add-comment-global/(?P<song_id>\d+)$', views.add_comment_global, name='add-comment-global'),
    # url(r'^add-comment-profile/(?P<song_id>\d+)/(?P<profile_id>\d+)$', views.add_comment_profile, name='add-comment-profile'),
    url(r'^logout$', auth_views.logout_then_login, name='logout'),
    url(r'^follow/(?P<profile_id>\d+)$', views.follow, name='follow'),
    url(r'^unfollow/(?P<profile_id>\d+)$', views.unfollow, name='unfollow'),
    url(r'^add-comment/(?P<song_id>\d+)$', views.add_comment, name='add-comment')
    # url(r'^workspace/(?P<id>\d+)$', views.workspace, name='workspace'),
]
