# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand
from django.core.urlresolvers import reverse

from ...auth import EmailTokenAuthBackend


class Command(BaseCommand):
    help = "E-mail login without sending the actual e-mail."

    def add_arguments(self, parser):
        parser.add_argument('email', type=str)

    def handle(self, email, **options):
        if '@' not in email:
            self.stderr.write("Failed. E-mail is mandatory.")
            return 1
        query_string = EmailTokenAuthBackend().issue(email)
        self.stdout.write("Complete login with: %s?%s" % (reverse('oneall-login'), query_string))
