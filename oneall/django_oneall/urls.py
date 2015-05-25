# -*- coding: utf-8 -*-
from django.conf.urls import url

from .views import oa_login, oa_logout, oa_profile, oa_nosocial


urlpatterns = [
    url('^login', oa_login, name='oneall-login'),
    url('^logout', oa_logout, name='oneall-logout'),
    url('^profile', oa_profile, name='oneall-profile'),
    url('^nosocial', oa_nosocial, name='oneall-nosocial')
]
