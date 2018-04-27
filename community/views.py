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
from django.db import transaction
from community.forms import *
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.utils import timezone

@login_required
def home(request):
    context = {}
    context['songs'] = Song.objects.all().order_by('-creation_time')
    context['comments'] = Comment.objects.all().order_by('creation_time')
    context['comment_form'] = CommentForm()
    return render(request, 'community/globalStream.html', context)

@login_required
def profile(request, profile_id):
    context = {}

    login_user_profile = get_object_or_404(Profile, user=request.user)
    result_profile = get_object_or_404(Profile, id=profile_id)
    context['result_profile'] = result_profile
    context['songs'] = result_profile.song_set.all().order_by('-creation_time')
    context['comments'] = Comment.objects.all().order_by('creation_time')
    context['comment_form'] = CommentForm()
    if login_user_profile == result_profile:
        followings = login_user_profile.followings.all()
        context['following_count'] = followings.count()
    else:
        followings = result_profile.followings.all()
        context['following_count'] = followings.count()
        if result_profile in login_user_profile.followings.all():
            context['followed'] = True
        else:
            context['followed'] = False
    return render(request, 'community/profile.html', context)

@login_required
@transaction.atomic
def profile_setting(request):
    context = {}

    if request.method == "POST" and request.FILES:
        new_profile = Profile.objects.get(user=request.user)
        form = UpdateProfileForm(request.POST, request.FILES, instance=new_profile)

        if not form.is_valid():
            print("form is not valid")
            context['form'] = form
        else:
            # new_profile.avatar_content_type = form.cleaned_data['avatar'].content_type
            # new_profile.header_image_content_type = form.cleaned_data['header_image'].file.content_type
            form.save()
            context['form'] = UpdateProfileForm(initial={"description":""})
        context['login_profile'] = Profile.objects.get(user=request.user)
        return render(request, 'community/profile-setting.html', context)

    # if request.method == "GET":
    else:
        # profile = Profile.objects.get(user=request.user)
        form = UpdateProfileForm(initial={"description":""})
        context['form'] = form
        context['login_profile'] = Profile.objects.get(user=request.user)
        return render(request, 'community/profile-setting.html', context)
    # context = {}
    # context['login_profile'] = request.user.profile
    # return render(request, 'community/profile-setting-pure-template.html', context)



@login_required
def following_users(request, profile_id):
    context = {}

    login_user_profile = get_object_or_404(Profile, user=request.user)
    result_profile = get_object_or_404(Profile, id=profile_id)
    context['result_profile'] = result_profile
    followings = result_profile.followings.all()
    context['following_count'] = followings.count()
    context['followings'] = followings

    if login_user_profile != result_profile:
        if result_profile in login_user_profile.followings.all():
            context['followed'] = True
        else:
            context['followed'] = False
    return render(request, 'community/following.html', context)

@login_required
def get_song(request, song_id):
    song = get_object_or_404(Song, id=song_id)

    if not song.songfile:
        raise Http404
    return HttpResponse(song.songfile, content_type=song.songfile_content_type)

@transaction.atomic
@login_required
def follow(request, profile_id):
    login_profile = request.user.profile
    curr_profile = get_object_or_404(Profile, id=profile_id)
    login_profile.followings.add(curr_profile)
    return redirect('profile', profile_id=profile_id)

@transaction.atomic
@login_required
def unfollow(request, profile_id):
    login_profile = request.user.profile
    curr_profile = get_object_or_404(Profile, id=profile_id)
    login_profile.followings.remove(curr_profile)
    return redirect('profile', profile_id=profile_id)

@transaction.atomic
@login_required
def add_comment_global(request, song_id):
    related_song = get_object_or_404(Song, id=song_id)
    new_comment = Comment(creator_profile=request.user.profile, parent_song=related_song)
    comment_form = CommentForm(request.POST, instance=new_comment)

    if comment_form.is_valid():
        comment_form.save()
    return redirect('home')

@transaction.atomic
@login_required
def add_comment_profile(request, song_id, profile_id):
    related_song = get_object_or_404(Song, id=song_id)
    new_comment = Comment(creator_profile=request.user.profile, parent_song=related_song)
    comment_form = CommentForm(request.POST, instance=new_comment)

    if comment_form.is_valid():
        comment_form.save()
    return redirect('profile', profile_id=profile_id)
