# -*- coding: utf-8 -*-
from django.conf.urls import url

from .views import oa_login, oa_logout, oa_profile


urlpatterns = [
    url('^login', oa_login, name='oneall_login'),
    url('^logout', oa_logout, name='oneall_logout'),
    url('^profile', oa_profile, name='oneall_profile'),
]
