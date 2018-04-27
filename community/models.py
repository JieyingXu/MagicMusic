# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from magicmusic.models import Workspace

DEFAULT_AVATAR_URL = "community/default-images/default-avatar.jpg"
DEFAULT_BG_URL = "community/default-images/default-background.jpg"
DEFAULT_COVER_URL = "community/default-images/default-cover.jpg"
DEFAULT_PROFILE_DESC = "The user didn't add a bio..."
DEFAULT_SONG_DESC = "Add some descriptions..."

# Each person has one profile
# and we directly list all the albums in Web UI
class Profile(models.Model):
    user = models.OneToOneField(User)
    avatar = models.ImageField(blank=True, upload_to="community/user-avatars", default=DEFAULT_AVATAR_URL)
    # avatar_content_type = models.CharField(max_length=50)
    header_image = models.ImageField(blank=True, upload_to="community/user-backgrounds", default=DEFAULT_BG_URL)
    # header_image_content_type = models.CharField(max_length=50)
    description = models.CharField(max_length=200, blank=True, default=DEFAULT_PROFILE_DESC)
    followings = models.ManyToManyField('self',
                                        related_name="follower_profile_set",
                                        blank=True,
                                        symmetrical=False)  # who am I following

# Album has many songs
# class Album(models.Model):
#     portfolio = models.ForeignKey(Profile)
    # name = models.CharField(max_length=100, blank=False)
    # description = models.CharField(max_length=200, blank=True, null=True)
    # cover_picture = models.FileField(blank=True, upload_to="userfiles/community/album-images")
    # creation_time = models.DateTimeField(auto_now_add=True)
    # genre = models.CharField(max_length=200, blank=False)


# Song Data Model has some metadata, a link to one wav/mp3 file and is connected
# with an original workspace
class Song(models.Model):
    liking_people = models.ManyToManyField(Profile, related_name="liking_people_set", blank=True)
    # album = models.ForeignKey(Album)
    creator = models.ForeignKey(Profile, blank=False)
    name = models.CharField(max_length=100, blank=False)
    description = models.CharField(max_length=200, blank=False, null=True)
    # length = models.IntegerField
    creation_time = models.DateTimeField(auto_now_add=True)
    songfile = models.CharField(max_length=256, blank=False)  #songfile name should be <username>_<songfilename>
    # songfile_content_type = models.CharField(max_length=50)
    workspace = models.OneToOneField(Workspace)
    #
    # likes = models.IntegerField
    # edit_counts = models.IntegerField

    cover = models.ImageField(blank=True, upload_to="community/song-covers", default=DEFAULT_COVER_URL)
    # cover_content_type = models.CharField(max_length=50)


# model for a comment, people can comment on a song
class Comment(models.Model):
    creator_profile = models.ForeignKey(Profile, related_name="comment_set")
    text = models.CharField(max_length=500)
    creation_time = models.DateTimeField(auto_now_add=True)
    parent_song = models.ForeignKey(Song)



