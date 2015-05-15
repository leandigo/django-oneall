# -*- coding: utf-8 -*-
from django.conf.urls import url

from .views import oa_login, oa_logout


urlpatterns = [
    url('^login', oa_login, name='oneall_login'),
    url('^logout', oa_logout, name='oneall_logout'),
]
