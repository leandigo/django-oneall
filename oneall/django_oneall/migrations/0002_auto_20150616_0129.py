# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


def remove_dashes_from_tokens(apps, _):
    for item in apps.get_model('django_oneall', 'OneAllUserIdentity').objects.iterator():
        item.user_token = item.user_token.replace('-', '')
        item.save()


class Migration(migrations.Migration):

    dependencies = [
        ('django_oneall', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(remove_dashes_from_tokens),
        migrations.AlterField(
            model_name='onealluseridentity',
            name='user_token',
            field=models.UUIDField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='onealluseridentity',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AlterField(
            model_name='onealluseridentity',
            name='raw',
            field=models.TextField(default='{}'),
        ),
        migrations.RenameModel(
            old_name='OneAllUserIdentity',
            new_name='SocialUserCache',
        ),
        migrations.AlterModelTable(
            name='socialusercache',
            table=None,
        ),
    ]
