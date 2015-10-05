# -*- coding: utf-8 -*-
from django import forms
from django.utils.translation import ugettext_lazy


class EmailForm(forms.Form):
    email = forms.EmailField(label=ugettext_lazy("E-mail"))
