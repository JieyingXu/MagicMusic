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
        objects = Workspace.objects.filter(workspace_group__users__in=[request.user])
        workspaces = []
        for e in objects:
            workspace = []
            workspace = {'name': e.name, 'id':e.id}
            workspaces.append(workspace);
        context = {'workspaces': workspaces}
        return render(request, 'magicmusic/mymusic.html', context)
    else:
        print("post\n")

@login_required
def addworkspace(request):
	# print("addworkspace\n")
	if request.method == 'GET':
		context = {'form': WorkspaceForm()}
		return render(request, 'magicmusic/addworkspace.html', context)
	else:
		newworkspace_form = WorkspaceForm(request.POST)
		with transaction.atomic():
			newworkspacegroup = WorkspaceGroup()
			newworkspacegroup.save()
			# print("newworkspacegroup id: " + str(newworkspacegroup.id))
			newworkspacegroup.users.add(request.user)
			# print("newworkspacegroup user: " + str(newworkspacegroup.users.all()[0]))
			newworkspacegroup.save()
		newworkspace = Workspace(workspace_group=newworkspacegroup,
						name=newworkspace_form.data['name'],
    					description=newworkspace_form.data['description'])
		newworkspace.save()
		# print("newworkspace user: " + str(newworkspace.name))
		return redirect(reverse('mymusic'))

@login_required
def workspace(request, id):
    print("workspace\n")
    if request.method == 'GET':
        objects = Workspace.objects.filter(id__exact=id)
        workspace = objects.all()[0]
    	# print("workspace is:"+str(workspace.id))
        tracks = []
        objects = Track.objects.filter(workspace__exact=workspace)
        for e in objects:
            track = {'instrument': e.instrument, 'trackid': e.id}
            # print("track instrument is:"+str(e.id))
            tracks.append(track);
        context = {'tracks': tracks, 'workspaceID':id}
        return render(request, 'magicmusic/workspace.html', context)
    else:
        objects = Workspace.objects.filter(id__exact=id)
        workspace = objects.all()[0]
        instrument = request.POST.getlist('instruments')[0]
        newtrack = Track(workspace=workspace,
        				name=request.POST.get('name'),
        				description=request.POST.get('description'),
                        instrument=instrument)
        newtrack.save()
        workspace.track_set.add(newtrack)
        workspace.save()
        tracks = []
        objects = Track.objects.filter(workspace__exact=workspace)
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
def profile(request):
	print("profile")

@login_required
def follower(request):
	print("follower")
