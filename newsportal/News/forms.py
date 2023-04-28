from django import forms
from django.core.exceptions import ValidationError
from allauth.account.forms import SignupForm
from django.contrib.auth.models import Group

from .models import Post


class PostForm(forms.ModelForm):
    post_text = forms.CharField(min_length=50)

    class Meta:
        model = Post
        fields = ['author', 'category', 'post_header', 'post_text']
        success_url = 'news/'

    def clean(self):
        cleaned_data = super().clean()
        post_header = cleaned_data.get('post_header')
        post_text = cleaned_data.get('post_text')

        if post_header == post_text:
            raise ValidationError(
                "Описание не должно быть идентично названию."
            )
        return cleaned_data


class BasicSignupForm(SignupForm):

    def save(self, request):
        user = super(BasicSignupForm, self).save(request)
        basic_group = Group.objects.get(name='Common')
        basic_group.user_set.add(user)
        return user
