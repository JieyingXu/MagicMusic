# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
# from authenticate.models import *
from django.contrib.auth.models import User

# Data model for Workspace Group, has many users and one workspace
class WorkspaceGroup(models.Model):
    users = models.ManyToManyField(User)

# Data model for Workspace, has many tracks
class Workspace(models.Model):
    workspace_group = models.OneToOneField(WorkspaceGroup)
    name = models.CharField(max_length=100, blank=False, null=True)
    description = models.CharField(max_length=200, blank=True, null=True)

# Data model for Workspace Track
class Track(models.Model):
    workspace = models.ForeignKey(Workspace)
    name = models.CharField(max_length=100, blank=False, null=True)
    description = models.CharField(max_length=200, blank=True, null=True)
    instrument = models.CharField(max_length=100, blank=False, null=True)
    blob = models.TextField(blank=True, null=True)
