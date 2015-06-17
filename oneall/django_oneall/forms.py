# -*- coding: utf-8 -*-
from django import forms
from django.utils.translation import ugettext_lazy as _

from .models import User


class LoginForm(forms.Form):  # TODO: encrypt this information over http
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


class RegisterForm(forms.Form):
    email = forms.EmailField(
        label=_("Email address"),
        max_length=30)
    username = forms.SlugField(
        label=_("User name"),
        help_text=_("Leave it empty to have it equal to the first part of your e-mail."),
        max_length=30,
        required=False)
    password1 = forms.CharField(
        label=_("Password"),
        help_text=_("Leave it empty to have it automatically generated (8 random characters)."),
        widget=forms.PasswordInput,
        required=False)
    password2 = forms.CharField(
        label=_("Confirm password"),
        widget=forms.PasswordInput,
        required=False)


class UserProfileForm(forms.ModelForm):
    model = User
