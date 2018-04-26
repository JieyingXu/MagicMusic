from django import forms
from django.forms import Textarea

from community.models import *

MAX_UPLOAD_SIZE = 2500000

class UpdateProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        exclude = (
            'user',
            'avatar_content_type',
            'header_image_content_type',
            'followings',
        )
        # widgets = {
        #     'description': Textarea(
        #         attrs={'class': "form-control", 'rows': "2"}),
        # }

    def clean_avatar(self):
        avatar = self.cleaned_data['avatar']
        if not avatar:
            raise forms.ValidationError('You must upload a picture')
        if not avatar.content_type or not avatar.content_type.startswith(
                'image'):
            raise forms.ValidationError('File type is not image')
        if avatar.size > MAX_UPLOAD_SIZE:
            raise forms.ValidationError(
                'File too big (max size is {0} bytes)'.format(MAX_UPLOAD_SIZE))
        return avatar

    def clean_header_image(self):
        header_image = self.cleaned_data['header_image']
        if not header_image:
            raise forms.ValidationError('You must upload a picture')
        if not header_image.content_type or not header_image.content_type.startswith(
                'image'):
            raise forms.ValidationError('File type is not image')
        if header_image.size > MAX_UPLOAD_SIZE:
            raise forms.ValidationError(
                'File too big (max size is {0} bytes)'.format(MAX_UPLOAD_SIZE))
        return header_image

