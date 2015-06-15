# -*- coding: utf-8 -*-
from random import randrange

from django.conf import settings
from django.template import Library

register = Library()


@register.inclusion_tag('header.html')
def oneall_header():
    return {'oneall_site_name': settings.ONEALL_SITE_NAME}


@register.inclusion_tag('login_widget.html')
def oneall_login_widget():
    return {
        'oneall_social_login_container_id': 'oneall_social_login_container_%d' % randrange(0x7fff),
        'oneall_settings': settings.ONEALL_LOGIN_WIDGET,
    }
