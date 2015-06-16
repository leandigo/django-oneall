# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('django_oneall', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='onealluseridentity',
            name='raw',
            field=models.TextField(default='{}'),
        ),
        migrations.AlterField(
            model_name='onealluseridentity',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AlterField(
            model_name='onealluseridentity',
            name='user_token',
            field=models.UUIDField(primary_key=True, serialize=False),
        ),
    ]
