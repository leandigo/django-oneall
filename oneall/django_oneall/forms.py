# -*- coding: utf-8 -*-
from django import forms

from .models import User


class LoginForm(forms.Form):  # TODO: encrypt this information over http
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


class UserProfileForm(forms.ModelForm):
    model = User
