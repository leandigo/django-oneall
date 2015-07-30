# -*- coding: utf-8 -*-
from django.contrib import admin

from .models import SocialUserCache


@admin.register(SocialUserCache)
class IdentityAdmin(admin.ModelAdmin):
    readonly_fields = ('raw',)
    list_display = ('user_token', 'user', 'raw')
