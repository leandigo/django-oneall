# -*- coding: utf-8 -*-
from base64 import urlsafe_b64decode, urlsafe_b64encode
from logging import getLogger
from uuid import UUID

from django import get_version
from django.contrib.auth.backends import ModelBackend
from django.http import QueryDict
from pyoneall import OneAll

from . import __version__
from .app import settings
from .models import SocialUserCache, EmailLoginToken, get_pseudo_random_user

log = getLogger(__name__)

# The worker to be used for authentication
oneall = OneAll(**settings.credentials)
oneall.set_version(__version__, 'django-oneall', get_version())


class BaseBackend(object):
    def __init__(self, existing_user=None):
        self.user = existing_user

    @classmethod
    def get_user(cls, user_id):
        """
        Retrieve user by user ID
        :param user_id: User ID
        """
        return ModelBackend().get_user(user_id)


class OneAllAuthBackend(BaseBackend):
    KEY = 'connection_token'

    def authenticate(self, connection_token, **_):
        """
        Performs authentication using a connection token. Creates and updates User and OneAllUserIdentity
        if necessary.
        :param str connection_token: OneAll connection token
        """
        oa_user = oneall.connection(connection_token).user

        if not settings.store_user_info:
            # Do not store any personally identifiable information.
            return get_pseudo_random_user(UUID(oa_user.user_token))

        # Check if user exists and create one if not
        try:
            identity = SocialUserCache.objects.get(user_token=oa_user.user_token)
            identity.refresh(raw=oa_user.identity)
            if self.user:
                identity.user = self.user  # override any existing link.
            identity.update_user_cache()
        except SocialUserCache.DoesNotExist:
            identity = SocialUserCache(user_token=oa_user.user_token,
                                       raw=str(oa_user.identity), user=self.user)
            identity.update_user_cache()

        # Return authenticated user
        return identity.user


class EmailTokenAuthBackend(BaseBackend):
    KEY = 'etk'
    login = None

    def issue(self, email):
        self.login = EmailLoginToken.issue(email)
        result = QueryDict(mutable=True)
        result[self.KEY] = urlsafe_b64encode(self.login.token.bytes)[:-2]
        return result

    def authenticate(self, **kwargs):
        if self.KEY in kwargs:
            token = UUID(bytes=urlsafe_b64decode(kwargs[self.KEY].encode('ascii') + b'=='))
            try:
                login = EmailLoginToken.consume(token)
            except EmailLoginToken.DoesNotExist:
                return None
            if not self.user:
                return login.produce_user()
            else:
                # this was an email change request!
                # TODO: check for existing users bearing the same address. can a merge happen? if not, what can?
                self.user.email = login.email
                self.user.save()
                return self.user
