from django.db import models
from django.conf import settings
from pyoneall.base import OADict

user_model = getattr(settings, 'AUTH_USER_MODEL', 'auth.User').split('.')
User = models.loading.get_model('.'.join(user_model[:-1]), user_model[-1])

class OneAllUserIdentity(models.Model):
    """
    OneAll User Identity Model
    Caches raw JSON corresponding with user's social identity allow instant retrieval of user details.
    """
    user_token = models.CharField(max_length=36, primary_key=True)
    raw = models.CharField(max_length=8192, default='{}')
    user = models.OneToOneField(User, related_name="identity", null=True)

    def __init__(self, *args, **kwargs):
        """
        Upon creation, creates attributes to correspond with the cached data in `raw`
        """
        super(self.__class__, self).__init__(*args, **kwargs)
        self.__dict__.update(OADict(**eval(self.raw)))

    def refresh(self, raw=None):
        """
        Refresh identity cache from OneAll
        """
        if not raw:
            from auth import oneall
            raw = oneall.user(self.user.username).identities.identity[0]
        raw.pop('id', None)
        raw.pop('user', None)
        self.raw = unicode(raw)
        self.__dict__.update(OADict(**eval(self.raw)))
        self.save()

    def update_user_cache(self):
        """
        Update selected fields in the User model from social identity
        """
        user = self.user if self.user else User()
        for field, values in getattr(settings, 'ONEALL_CACHE_FIELDS', {}).iteritems():
            for value in values:
                try:
                    setattr(user, field, eval('self.%s' % value))
                    print eval('self.%s' % value)
                except Exception as e:
                    print e
        user.save()
        if not self.user:
            self.user = user
            self.save()

    class Meta:
        db_table = getattr(settings, 'ONEALL_CACHE_TABLE', 'oneall_cache')
