# -*- coding: utf-8 -*-
from django.conf import settings

from ..connection import OneAll
from .models import User, SocialUserCache


# The worker to be used for authentication
oneall = OneAll(settings.ONEALL_SITE_NAME, settings.ONEALL_PUBLIC_KEY, settings.ONEALL_PRIVATE_KEY)


class OneAllAuthBackend(object):
    """
    OneAll Authentication Backend.
    """

    @classmethod
    def authenticate(cls, connection_token, **_):
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
                identity.update_user_cache()
        except SocialUserCache.DoesNotExist:
            identity = SocialUserCache(user_token=oa_user.user_token, raw=str(oa_user.identity))
            identity.update_user_cache()

        # Return authenticated user
        return identity.user

    @classmethod
    def get_user(cls, user_id):
        """
        Retrieve user by user ID
        :param user_id: User ID
        """
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
