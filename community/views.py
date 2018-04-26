# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

# Create your views here.

# -*- coding: utf-8 -*-

from django.shortcuts import render

# Create your views here.

from community.models import *
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, Http404
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.utils import timezone

@login_required
def home(request):
    context = {}
    songs = Song.objects.all().order_by('-creation_time')
    comments = Comment.objects.all().order_by('creation_time')
    return render(request, 'community/globalStream.html', context)

@login_required
def profile(request, user_id):
    context = {}

    login_user_profile = get_object_or_404(Profile, user=request.user)
    result_profile = get_object_or_404(Profile, user__id=user_id)
    context['result_profile'] = result_profile
    
    return render(request, 'community/profile.html', {})

@login_required
def profile_setting(request):
    pass

@login_required
def following_users(request):
    pass

@login_required
def get_profile_avatar(request, user_id):
    profile = get_object_or_404(Profile, user__id=user_id)

    if not profile.avatar:
        raise Http404
    return HttpResponse(profile.avatar, content_type=profile.avatar_content_type)

@login_required
def get_profile_bg(request, user_id):
    profile = get_object_or_404(Profile, user__id=user_id)

    if not profile.avatar:
        raise Http404
    return HttpResponse(profile.avatar, content_type=profile.avatar_content_type)

@login_required
def get_song_cover(request, song_id):
    song = get_object_or_404(Song, id=song_id)

    if not song.cover:
        raise Http404
    return HttpResponse(song.cover, content_type=song.cover_content_type)

@login_required
def get_song(request, song_id):
    song = get_object_or_404(Song, id=song_id)

    if not song.songfile:
        raise Http404
    return HttpResponse(song.songfile, content_type=song.songfile_content_type)
