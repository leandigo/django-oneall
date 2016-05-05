# -*- coding: utf-8 -*-
from json import dumps

from django.db.models import get_user_model
from django.template import Library
from django.utils.html import escape
from django.utils.safestring import mark_safe

from ..app import settings
from ..models import SocialUserCache

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
    if isinstance(user, get_user_model()):
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


@register.inclusion_tag('oneall/social_sharing.html')
def oneall_share(layout='s', **kwargs):
    """
    This tag display the `Social Sharing`_ widget.

    .. _Social Sharing: https://www.oneall.com/services/social-sharing/

    Don't forget to include ``{% oneall_header %}``!

    :param layout: Button layout as defined by the Social Sharing Wizard.
    :param kwargs: Social link arguments.
    """
    layout = str(layout).lower()
    if layout not in 'smlhv':
        raise ValueError("Invalid layout (%s). Must be one of S M L H or V." % layout)
    args = ' '.join(('data-%s="%s"' % (k, escape(v)) for k, v in kwargs.items()))
    return {
        'layout': layout,
        'arguments': mark_safe(args),
        'networks': settings.share_widget['networks']
    }
