# -*- coding: utf-8 -*-
from json import dumps

from django.conf import settings
from django.template import Library
from django.utils.safestring import mark_safe

from ..models import User, OneAllUserIdentity

register = Library()

default_widget_settings = {
    None: "This is a dummy marker to indicate that the Django settings haven't been loaded yet.",
    'providers': 'google facebook twitter openid'.split(),
}


@register.inclusion_tag('oneall/header.html')
def oneall_header():
    """
    OneAll required script.

    This must go in the ``<head>...</head>`` section of your templates,
    otherwise widgets won't load.
    """
    return {'oneall_site_name': settings.ONEALL_SITE_NAME}


@register.inclusion_tag('oneall/social_login.html')
def oneall_social_login(user=None, **kwargs):
    """
    This tag displays the Social Login or Social Link widget.

    Don't forget to include ``{% oneall_header %}``!

    :param user: Logged in user for Social Link mode; if not provided, it's Social Login mode.
    :param kwargs: Widget options as documented by OneAll. For example, ``grid_sizes=[8,5]``
    """
    if None in default_widget_settings:
        del default_widget_settings[None]
        if hasattr(settings, 'ONEALL_LOGIN_WIDGET'):
            default_widget_settings.update(settings.ONEALL_LOGIN_WIDGET)
        for key, value in default_widget_settings.items():
            default_widget_settings[key] = mark_safe(dumps(value))
    if kwargs:
        widget_settings = dict(default_widget_settings)
        if isinstance(user, User):
            oaid = OneAllUserIdentity.objects.filter(user=user).first()
            kwargs['user_token'] = str(oaid.user_token)
        for key, value in kwargs.items():
            widget_settings[key] = mark_safe(dumps(value))
    else:
        widget_settings = default_widget_settings
    return {'oneall_settings': widget_settings}
