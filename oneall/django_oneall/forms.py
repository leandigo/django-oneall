# -*- coding: utf-8 -*-
from django import forms

from .models import User


class EmailForm(forms.Form):
    email = forms.EmailField()


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name')
