# -*- coding: utf-8 -*-
from json import dumps

from django.template import Library
from django.utils.safestring import mark_safe

from ..app import settings
from ..models import User, SocialUserCache

register = Library()


@register.inclusion_tag('oneall/header.html')
def oneall_header():
    """
    OneAll required script.

    This must go in the ``<head>...</head>`` section of your templates,
    otherwise widgets won't load.
    """
    return {'oneall_site_name': settings.credentials['site_name']}


@register.inclusion_tag('oneall/social_login.html')
def oneall_social_login(user=None, **kwargs):
    """
    This tag displays the Social Login or Social Link widget.

    Don't forget to include ``{% oneall_header %}``!

    :param user: Logged in user for Social Link mode; if not provided, it's Social Login mode.
    :param kwargs: Widget options as documented by OneAll. For example, ``grid_sizes=[8,5]``
    """
    if isinstance(user, User):
        social_user = SocialUserCache.objects.filter(user=user).first()
        if social_user:
            kwargs['user_token'] = str(social_user.user_token)
        else:
            user = None  # no cached social user, thus revert to social login mode
    widget_settings = {}
    for key, value in settings.login_widget(kwargs).items():
        widget_settings[key] = mark_safe(dumps(value))
    return {
        'settings': widget_settings,
        'mode': 'social_link' if user else 'social_login',
    }
