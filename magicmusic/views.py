# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect, get_object_or_404
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
from django.db import transaction
from django.utils import timezone
from django.http import HttpResponse, Http404

from magicmusic.models import *
from magicmusic.forms import *

@login_required
def mymusic(request):
    if request.method == 'GET':
        objects = Song.objects.filter(user__exact=request.user)
        songs = []
        for e in objects:
            workspace = e.workspace_set.all()[0]
            """print("song name:"+str(e.name))"""
            song = {'name': e.name, 'id':workspace.id}
            songs.append(song);
        context = {'songs': songs}
        return render(request, 'magicmusic/mymusic.html', context)
    else:
        print("post\n")

@login_required
def addsong(request):
    print("addsong\n")
    if request.method == 'GET':
        context = {'form': SongForm()}
        return render(request, 'magicmusic/addsong.html', context)
    else:
    	newsong_form = SongForm(request.POST)
    	newsong = Song(user=request.user,
    					name=newsong_form.data['name'],
    					description=newsong_form.data['description'])
    	newsong.save()
        newworkspace = Workspace(user=request.user)
        newworkspace.save()
        newsong.workspace_set.add(newworkspace)
        newsong.save()
        """print("newsong name is:"+str(newsong.name)+"\n")
        print("newworkspace is:"+str(newworkspace.id))"""
        return redirect(reverse('mymusic'))

@login_required
def workspace(request, id):
    print("workspace\n")
    if request.method == 'GET':
        objects = Workspace.objects.filter(id__exact=id)
        workspace = objects.all()[0]
    	"""print("workspace is:"+str(workspace.id))"""
        tracks = []
        objects = Track.objects.filter(user__exact=request.user)
        for e in objects:
            track = {'instrument': e.instrument, 'trackid': e.id}
            print("track instrument is:"+str(e.id))
            tracks.append(track);
        context = {'tracks': tracks, 'workspaceID':id}
        return render(request, 'magicmusic/workspace.html', context)
    else:
        objects = Workspace.objects.filter(id__exact=id)
        workspace = objects.all()[0]
        instrument = request.POST.getlist('instruments')[0]
        newtrack = Track(user=request.user,
                        instrument=instrument)
        newtrack.save()
        workspace.track_set.add(newtrack)
        workspace.save()
        tracks = []
        objects = Track.objects.filter(user__exact=request.user)
        for e in objects:
            track = {'instrument': e.instrument, 'trackid': e.id}
            tracks.append(track);
        context = {'tracks': tracks, 'workspaceID':id}
        return render(request, 'magicmusic/workspace.html', context)

@login_required
def track(request, id):
    print("track")
    if request.method == 'GET':
        objects = Track.objects.filter(id__exact=id)
        track = objects.all()[0]
        print("track is:"+str(track.id))
        context = {'trackID':id}
        return render(request, 'magicmusic/track.html', context)
    else:
        print("post")

@login_required
def follower(request):
    print("follower\n")

@login_required
def profile(request):
    print("profile\n")

def register(request):
    context = {}

    # Just display the registration form if this is a GET request.
    if request.method == 'GET':
        context['form'] = RegistrationForm()
        return render(request, 'magicmusic/register.html', context)

    # Creates a bound form from the request POST parameters and makes the 
    # form available in the request context dictionary.
    form = RegistrationForm(request.POST)
    context['form'] = form

    # Validates the form.
    if not form.is_valid():
        return render(request, 'magicmusic/register.html', context)

    # At this point, the form data is valid.  Register and login the user.
    new_user = User.objects.create_user(username=form.cleaned_data['username'], 
                                        password=form.cleaned_data['password1'],
                                        first_name=form.cleaned_data['first_name'],
                                        last_name=form.cleaned_data['last_name'])
    new_user.save()

    newprofile = ProfileEntry(user=new_user,
                              update_time=timezone.now(),
                              username=form.cleaned_data['username'], 
                              first_name=form.cleaned_data['first_name'],
                              last_name=form.cleaned_data['last_name'])
    newprofile.save()

    # Logs in the new user and redirects to his/her todo list
    new_user = authenticate(username=form.cleaned_data['username'],
                            password=form.cleaned_data['password1'])
    login(request, new_user)
    return redirect(reverse('mymusic'))

