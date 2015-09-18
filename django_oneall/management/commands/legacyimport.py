# -*- coding: utf-8 -*-
from uuid import UUID

from django.conf import settings
from django.core.management.base import BaseCommand
from django.db import models, OperationalError, connection

from ...models import SocialUserCache


class Command(BaseCommand):
    help = "Loads OneAll data from a legacy table (oneall_cache table from django-oneall v0.1)."

    class LegacyOneAllCache(models.Model):
        user_token = models.CharField(max_length=36, primary_key=True)
        raw = models.CharField(max_length=8192)
        user = models.ForeignKey(to=settings.AUTH_USER_MODEL)

        class Meta(object):
            db_table = 'oneall_cache'

    def handle(self, *args, **options):
        try:
            src = self.LegacyOneAllCache.objects
            self.stdout.write("%d users to migrate." % src.count())
        except OperationalError as e:
            self.stderr.write("Couldn't import. %s" % e)
            return
        cok = cbad = 0
        for oldrow in src.iterator():
            try:
                newid = UUID(oldrow.user_token)
                newrow = SocialUserCache(user_token=newid, raw=oldrow.raw, user=oldrow.user)
                newrow.save()
                cok += 1
            except ValueError:
                cbad += 1
                self.stderr.write("Invalid UUID <%s>", oldrow.user_token)
        self.stdout.write("Done. %d ok, %d failed." % (cok, cbad))
        if cbad:
            self.stdout.write("Import complete with errors. Keeping legacy table.")
        else:
            self.stdout.write("Import complete without errors. Deleting legacy table.")
            with connection.schema_editor() as schema_editor:
                schema_editor.delete_model(self.LegacyOneAllCache)
