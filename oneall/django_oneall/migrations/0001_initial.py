# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import uuid
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='SocialUserCache',
            fields=[
                ('user_token', models.UUIDField(serialize=False, primary_key=True)),
                ('raw', models.TextField(default='{}')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='EmailLoginToken',
            fields=[
                ('token', models.UUIDField(serialize=False, default=uuid.uuid4, primary_key=True)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('created', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]
