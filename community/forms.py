from django import forms
from django.forms.widgets import TextInput

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
                attrs={'class':"form-control comment-textbox"}
            )
        }

