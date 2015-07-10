# -*- coding: utf-8 -*-
from uuid import UUID

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.core.urlresolvers import reverse

from ...auth import EmailTokenAuthBackend
from ...models import SocialUserCache


class Command(BaseCommand):
    help = "Sets that user as super user. To create it too, use e-mail login."

    def add_arguments(self, parser):
        parser.add_argument('user', type=str, help="User ID, e-mail, or OneAll identity UUID.")

    def _extract_user(self, user):
        user_model = get_user_model()
        try:
            return user_model.objects.get(id=int(user))
        except (ValueError, user_model.DoesNotExist):
            pass
        try:
            return SocialUserCache.objects.get(user_token=UUID(user)).user
        except (ValueError, SocialUserCache.DoesNotExist):
            pass
        if '@' in user:
            auth = EmailTokenAuthBackend()
            self.stdout.write("Login with: %s?%s" % (reverse('oneall-login'), auth.issue(user)))
            return auth.login.produce_user()
        self.stdout.write("User <%s> not found." % user)

    def handle(self, user, **options):
        user = self._extract_user(user)
        if not user:
            return
        user.is_active = True
        user.is_staff = True
        user.is_superuser = True
        user.save()
        self.stdout.write("User #%d, email=%s is now super user." % (user.id, user.email))
