# -*- coding: utf-8 -*-
from datetime import timedelta

from django.conf import settings as django_settings

try:
    from django.contrib.auth import get_user_model
except ImportError:
    from django.db.models import get_user_model


class MissingOneAllSettings(KeyError):
    def __init__(self, msg=None):
        msg = 'Missing or invalid settings. Check django-oneall documentation for further info. ' + (msg or '')
        super(MissingOneAllSettings, self).__init__(msg)


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
        self._default_share_widget = {
            None: "This is a dummy marker to indicate that the Django settings haven't been loaded yet.",
            'providers': 'linkedin twitter facebook'.split(),
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
    def share_widget(self):
        """ Provides the share widget configuration. """
        if None in self._default_share_widget:
            del self._default_share_widget[None]
            self._default_share_widget.update(self._settings.get('share_widget', {}))
        return self._default_share_widget

    @property
    def store_user_info(self):
        """ Whether to store personally identifiable information from users. Defaults to True. """
        return bool(self._settings.get('store_user_info', True))

    @property
    def max_username_length(self):
        """ Maximum length of pseudorandom username generated when store_user_info=False is set.  Defaults to the max_length of the username field introspected by get_user_model)

            Django 1.10 included a migration which updated the max_length of the username field from 30 to 150 chars.  If you used django-oneall with older Django versions  and are upgrading to Django>=1.10, 
            you will want to set the value of this to 30 (or whatever max_length your custom User model may have) so that your existing user accounts are not mis-identified
        """
        user_model = get_user_model()
        fld_len = user_model._meta.get_field('username').max_length
        max_len = int(self._settings.get("max_username_length", fld_len))
        if max_len > fld_len:
            raise MissingOneAllSettings("OneAll setting 'max_username_length' is set to value %d, which is greater than the database field's length: %d" % (max_len, fld_len))
        return max_len

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
