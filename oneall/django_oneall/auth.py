# -*- coding: utf-8 -*-
from datetime import timedelta

from django.conf import settings
from django.contrib.auth.backends import ModelBackend
from django.core.signing import TimestampSigner

from ..connection import OneAll
from .models import SocialUserCache, produce_user_from_email

# The worker to be used for authentication
oneall = OneAll(settings.ONEALL_SITE_NAME, settings.ONEALL_PUBLIC_KEY, settings.ONEALL_PRIVATE_KEY)


class BaseBackend(object):
    @classmethod
    def get_user(cls, user_id):
        """
        Retrieve user by user ID
        :param user_id: User ID
        """
        return ModelBackend().get_user(user_id)


class OneAllAuthBackend(BaseBackend):
    def __init__(self, existing_user=None):
        self.user = existing_user

    def authenticate(self, connection_token, **_):
        """
        Performs authentication using a connection token. Creates and updates User and OneAllUserIdentity
        if necessary.
        :param str connection_token: OneAll connection token
        """
        oa_user = oneall.connection(connection_token).user

        # Check if user exists and create one if not
        try:
            identity = SocialUserCache.objects.get(user_token=oa_user.user_token)
            if getattr(settings, 'ONEALL_REFRESH_CACHE_ON_AUTH', True):
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
    _signer = None

    @property
    def signer(self) -> TimestampSigner:
        if not EmailTokenAuthBackend._signer:
            EmailTokenAuthBackend._signer = TimestampSigner()
        return EmailTokenAuthBackend._signer

    def issue(self, email):
        return {self.KEY: self.signer.sign(email)}

    def authenticate(self, **kwargs):
        if self.KEY in kwargs:
            token = kwargs[self.KEY]
            # The next line of code can raise BadSignature and SignatureExpired.
            # This will stop the authentication on its tracks and it will not keep trying on other backends.
            email = self.signer.unsign(token, max_age=timedelta(hours=3))
            return produce_user_from_email(email)
