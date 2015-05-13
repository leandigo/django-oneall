# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url

urlpatterns = patterns(
    '',  # TODO: Discover what this is for.
    url(r'^auth/$', 'oneall.views.oneall_auth', name='oneall_auth'),
)
