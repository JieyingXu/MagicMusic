from django import forms
from django.forms.widgets import *

from community.models import *

MAX_UPLOAD_SIZE = 2500000

class UpdateProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        exclude = (
            'user',
            # 'avatar_content_type',
            # 'header_image_content_type',
            'followings',
        )
        # widgets = {
        #     'description': Textarea(
        #         attrs={'class': "form-control", 'rows': "2"}),
        # }
        widgets = {
            'avatar': ClearableFileInput(attrs={'class': "my-file-input"}),
            'header_image': ClearableFileInput(attrs={'class': "my-file-input"}),
            'description': Textarea(attrs={'class': "form-control my-text-input",
                                           'rows': "5",
                                           'placeholder': "Say something about yourself..."})
        }

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        exclude = (
            'creator_profile',
            'creation_time',
            'parent_song',
        )
        widgets = {
            'text' : TextInput(
                attrs={'class':"form-control comment-textbox",
                       'placeholder': "write a comment..."}
            )
        }

class SongForm(forms.ModelForm):
    class Meta:
        model = Song
        exclude = (
            'liking_people',
            'songfile',
            'songfile_content_type',
            'creator',
            'likes',
            'edit_counts',
            'cover',
            'creation_time',
            'workspace',
        )