# -*- coding: utf-8 -*-
from django.conf import settings
from django.contrib.auth.backends import ModelBackend

from ..connection import OneAll
from .models import User, SocialUserCache


# The worker to be used for authentication
oneall = OneAll(settings.ONEALL_SITE_NAME, settings.ONEALL_PUBLIC_KEY, settings.ONEALL_PRIVATE_KEY)


class OneAllAuthBackend(object):
    """
    OneAll Authentication Backend.
    """
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

    @classmethod
    def get_user(cls, user_id):
        """
        Retrieve user by user ID
        :param user_id: User ID
        """
        return ModelBackend().get_user(user_id)
