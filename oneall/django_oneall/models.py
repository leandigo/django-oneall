# -*- coding: utf-8 -*-
from re import match, sub

from django.contrib.auth.models import User
from django.db import models

from ..base import OADict


class SocialUserCache(models.Model):
    """
    OneAll User Identity Model
    Caches raw JSON corresponding with user's social identity allow instant retrieval of user details.
    """
    user_token = models.UUIDField(primary_key=True)
    raw = models.TextField(default='{}')
    user = models.ForeignKey(User, null=True)

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
            from .auth import oneall

            raw = oneall.user(self.user.username).identities.identity[0]
        raw.pop('id', None)
        raw.pop('user', None)
        self.raw = str(raw)
        self.__dict__.update(OADict(**eval(self.raw)))
        self.save()

    def update_user_cache(self):
        """
        Update selected fields in the User model from social identity
        """
        if 'emails' in self.__dict__ and self.emails:
            email = self.emails[0].value
            if not self.user:
                self.user = User.objects.filter(email=email).first() or User(email=email)
            else:
                self.user.email = email
        if not self.user:
            self.user = User()
        if 'name' in self.__dict__ and 'givenName' in self.name:
            self.user.first_name = self.name.givenName
        if 'name' in self.__dict__ and 'familyName' in self.name:
            self.user.last_name = self.name.familyName
        if not self.user.username:
            self.user.username = _find_unique_username(self.preferredUsername)
        self.user.save()
        self.save()


def produce_user_from_email(email):
    user = User.objects.filter(email=email).first()
    if not user:
        preferred_username = sub(r'@.*$', '', email)
        user = User(email=email, username=_find_unique_username(preferred_username))
        user.save()
    return user


def _find_unique_username(current: str):
    """
    Checks wether given username is unique.
    If not unique or not given, tries to derive a new username that is.
    """
    exists = lambda n: User.objects.filter(username=n).exists()
    if current and not exists(current):
        return current
    prefix, suffix = match(r'^(.+?)(\d*)$', current or 'user').groups()
    suffix = int(suffix or 0) + 1
    current = prefix + str(suffix)
    while exists(current):
        suffix += 1
        current = prefix + str(suffix)
    return current
