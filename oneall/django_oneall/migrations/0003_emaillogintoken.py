# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('django_oneall', '0002_auto_20150616_0129'),
    ]

    operations = [
        migrations.CreateModel(
            name='EmailLoginToken',
            fields=[
                ('token', models.UUIDField(serialize=False, default=uuid.uuid4, primary_key=True)),
                ('email', models.EmailField(unique=True, max_length=254)),
                ('created', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]
