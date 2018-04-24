# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

# Create your views here.

# -*- coding: utf-8 -*-

from django.shortcuts import render

# Create your views here.

from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.utils import timezone

@login_required
def home(request):
    return render(request, 'community/globalStream.html', {})

@login_required
def profile(request):
    return render(request, 'community/profile.html', {})

@login_required
def profile_setting(request):
    pass

@login_required
def following_users(request):
    pass


