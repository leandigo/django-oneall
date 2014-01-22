from pyoneall import OneAll
from models import User
from django.conf import settings
from django.db.models import get_model

OneAllUserIdentity = get_model('django_oneall', 'OneAllUserIdentity')

# The worker to be used for authentication
oneall = OneAll(settings.ONEALL_SITE_NAME, settings.ONEALL_PUBLIC_KEY, settings.ONEALL_PRIVATE_KEY)

class OneAllAuthBackend(object):
    """
    OneAll Authentication Backend.
    """
    def authenticate(self, token):
        """
        Performs authentication using a connection token. Creates and updates User and OneAllUserIdentity
        if necessary.
        :param str token: OneAll connection token
        """
        oa_user = oneall.connection(token).user

        # Check if user exists and create one if not
        identity, created = OneAllUserIdentity.objects.get_or_create(
            user_token=oa_user.user_token,
            raw=unicode(oa_user.identity)
        )

        # Update cache for new users and for existing users if setting is provided
        if created:
            identity.update_user_cache()
        elif getattr(settings, 'ONEALL_REFRESH_CACHE_ON_AUTH', True):
            identity.refresh(raw=oa_user.identity)
            identity.update_user_cache()

        # Return authenticated user
        return identity.user

    def get_user(self, user_id):
        """
        Retrieve user by user ID
        :param user_id: User ID
        """
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
