# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='OneAllUserIdentity',
            fields=[
                ('user_token', models.CharField(primary_key=True, max_length=36, serialize=False)),
                ('raw', models.CharField(default='{}', max_length=8192)),
                ('user', models.OneToOneField(related_name='identity', null=True, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'oneall_cache',
            },
        ),
    ]
