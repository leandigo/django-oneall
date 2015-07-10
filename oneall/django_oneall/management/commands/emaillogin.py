# -*- coding: utf-8 -*-
from smtplib import SMTPResponseException

from django.core.mail import EmailMessage
from django.core.management.base import BaseCommand
from django.core.urlresolvers import reverse

from ...auth import EmailTokenAuthBackend


class Command(BaseCommand):
    help = "Issues an e-mail login token."

    def add_arguments(self, parser):
        parser.add_argument('-s', '--send', dest='send', action='store_true',
                            help="Actually e-mail the token instead of only displaying it.")
        parser.add_argument('email', type=str)

    def handle(self, email, send, **options):
        if '@' not in email:
            self.stderr.write("Failed. E-mail is mandatory.")
            return
        query_string = EmailTokenAuthBackend().issue(email)
        msg = "Complete login with: %s?%s" % (reverse('oneall-login'), query_string)
        self.stdout.write(msg)
        if send:
            mail = EmailMessage()
            mail.to = [email]
            mail.subject = 'Login Test'
            mail.body = msg
            try:
                sent = mail.send()
                self.stdout.write("Sent %d message." % sent)
            except SMTPResponseException as e:
                self.stderr.write("SMTP %d %s" % (e.smtp_code, e.smtp_error.decode('latin9')))
            except OSError as e:
                self.stderr.write("Conn %s" % e)
