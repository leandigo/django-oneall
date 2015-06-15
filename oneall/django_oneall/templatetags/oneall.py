# -*- coding: utf-8 -*-
from json import dumps

from django.conf import settings
from django.template import Library
from django.utils.safestring import mark_safe

register = Library()

default_widget_settings = {
    None: "This is a dummy marker to indicate that the Django settings haven't been loaded yet.",
    'providers': 'google facebook twitter openid'.split(),
}


@register.inclusion_tag('oneall/header.html')
def oneall_header():
    return {'oneall_site_name': settings.ONEALL_SITE_NAME}


@register.inclusion_tag('oneall/login_widget.html')
def oneall_login_widget(**kwargs):
    if None in default_widget_settings:
        del default_widget_settings[None]
        if hasattr(settings, 'ONEALL_LOGIN_WIDGET'):
            default_widget_settings.update(settings.ONEALL_LOGIN_WIDGET)
        for key, value in default_widget_settings.items():
            default_widget_settings[key] = mark_safe(dumps(value))
    if kwargs:
        widget_settings = dict(default_widget_settings)
        for key, value in kwargs.items():
            widget_settings[key] = mark_safe(dumps(value))
    else:
        widget_settings = default_widget_settings
    return {'oneall_settings': widget_settings}
