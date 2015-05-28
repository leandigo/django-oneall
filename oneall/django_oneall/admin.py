# -*- coding: utf-8 -*-
from django.contrib import admin

from .models import *


@admin.register(OneAllUserIdentity, app_label='oneall')
class IdentityAdmin(admin.ModelAdmin):
    readonly_fields = ('raw',)
    list_display = ('user_token', 'user', 'raw')
