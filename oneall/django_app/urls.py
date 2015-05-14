# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url

urlpatterns = patterns(
    '',
    url('', 'oneall.views.oneall_auth', name='oneall_auth'),
)
