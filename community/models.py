# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from magicmusic.models import Workspace


# Each person has one profile
# and we directly list all the albums in Web UI
class Profile(models.Model):
    user = models.OneToOneField(User)
    avatar = models.FileField(blank=True, upload_to="userfiles/community/avatar-images")
    avatar_content_type = models.CharField(max_length=50)
    header_image = models.FileField(blank=True, upload_to="userfiles/community/header-images")
    header_image_content_type = models.CharField(max_length=50)
    description = models.CharField(max_length=200, blank=True, null=True)
    followings = models.ManyToManyField('self',
                                        related_name="follower_profile_set",
                                        blank=True,
                                        symmetrical=False)  # who am I following


# Album has many songs
class Album(models.Model):
    portfolio = models.ForeignKey(Profile)
    name = models.CharField(max_length=100, blank=False)
    description = models.CharField(max_length=200, blank=True, null=True)
    cover_picture = models.FileField(blank=True, upload_to="userfiles/community/album-images")
    creation_time = models.DateTimeField(auto_now_add=True)
    genre = models.CharField(max_length=200, blank=False)


# Song Data Model has some metadata, a link to one wav/mp3 file and is connected
# with an original workspace
class Song(models.Model):
    album = models.ForeignKey(Album)
    name = models.CharField(max_length=100, blank=False)
    description = models.CharField(max_length=200, blank=True, null=True)
    length = models.IntegerField
    creation_time = models.DateTimeField(auto_now_add=True)
    songfile = models.FileField(blank=True, upload_to="userfiles/community/songfiles")  #songfile name should be <username>_<songfilename>
    songfile_content_type = models.CharField(max_length=50)
    workspace = models.OneToOneField(Workspace)
    likes = models.IntegerField
    played_counts = models.IntegerField


# model for a comment, people can comment on a song
class Comment(models.Model):
    user = models.ForeignKey(Profile, related_name="comment_set")
    text = models.CharField(max_length=500)
    creation_time = models.DateTimeField(auto_now_add=True)
    parent_song = models.ForeignKey(Song)



