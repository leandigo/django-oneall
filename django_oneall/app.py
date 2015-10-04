# -*- coding: utf-8 -*-
from datetime import timedelta

from django.conf import settings as django_settings


class MissingOneAllSettings(KeyError):
    def __init__(self, msg=None):
        msg = 'Missing or invalid settings. Check django-oneall documentation for further info. ' + (msg or '')
        super().__init__(msg)


class AppSettings(object):
    def __init__(self):
        if not hasattr(django_settings, 'ONEALL'):
            raise MissingOneAllSettings
        self._settings = django_settings.ONEALL
        if not isinstance(self._settings, dict):
            raise MissingOneAllSettings
        self._default_login_widget = {
            None: "This is a dummy marker to indicate that the Django settings haven't been loaded yet.",
            'providers': 'google facebook twitter openid'.split(),
        }

    @property
    def credentials(self):
        """ Provides the credentials dictionary for the OneAll connection. """
        try:
            return self._settings['credentials']
        except KeyError:
            raise MissingOneAllSettings('OneAll site credentials missing.')

    def login_widget(self, overlay=None):
        """ Provides the login widget settings as a dictionary, with an optional overlay. """
        if None in self._default_login_widget:
            del self._default_login_widget[None]
            self._default_login_widget.update(self._settings.get('login_widget', {}))
        if overlay:
            result = dict(self._default_login_widget)
            result.update(overlay)
            return result
        else:
            return self._default_login_widget

    @property
    def store_user_info(self):
        """ Whether to store personally identifiable information from users. Defaults to True. """
        return bool(self._settings.get('store_user_info', True))

    @property
    def token_expiration(self):
        """ The amount of time an e-mail login token is valid for. """
        expires = self._settings.get('email_token_expiration_hours', 3)
        return timedelta(hours=expires)

    @property
    def default_url(self):
        """ Default redirect URL after login if ``next`` is not provided. This is just a standard Django setting. """
        return django_settings.LOGIN_REDIRECT_URL  # Can be assumed to be set.


settings = AppSettings()
