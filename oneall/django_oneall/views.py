# -*- coding: utf-8 -*-
from json import dumps
from logging import getLogger

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.utils.safestring import mark_safe
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login, logout, views
from django.http import HttpRequest, HttpResponse

from .models import User, OneAllUserIdentity

log = getLogger(__name__)
default_settings = {'providers': 'google facebook twitter openid'.split()}


@csrf_exempt
def oa_login(request: HttpRequest) -> HttpResponse:
    """
    Display and callback view for OneAll Authentication.
    """
    oa_settings = dict(default_settings)
    if hasattr(settings, 'ONEALL_LOGIN_WIDGET'):
        oa_settings.update(settings.ONEALL_LOGIN_WIDGET)
    for key, value in oa_settings.items():
        oa_settings[key] = mark_safe(dumps(value))
    context = {
        'oa_site_name': settings.ONEALL_SITE_NAME,
        'login_failed': False,
        'oneall_settings': oa_settings,
    }
    if request.method == 'POST':
        connection_token = request.POST['connection_token']
        user = authenticate(token=connection_token)
        if user:
            login(request, user)
            response = redirect(request.GET.get('next') or settings.LOGIN_REDIRECT_URL)
            response.status_code = 303  # See Other
            return response
        else:
            context['login_failed'] = True
    return render(request, 'oneall/login.html', context)


def oa_logout(request: HttpRequest) -> HttpResponse:
    """
    Logs out the user and takes them somewhere if requested.
    """
    logout(request)
    url = request.GET.get('next')
    if url:
        response = redirect(url)
        response.status_code = 303  # See Other
        return response
    else:
        return render(request, 'oneall/logout.html')


@login_required
def oa_profile(request: HttpRequest) -> HttpResponse:
    """
    View to display logged in user profile along with their OneAll identity.
    """
    context = {
        'user': request.user,
        'identity': OneAllUserIdentity.objects.filter(user=request.user).first(),
    }
    return render(request, 'oneall/profile.html', context)


def oa_nosocial(request: HttpRequest) -> HttpResponse:
    """
    This is an alternative login page, for people who directly request no integration.

    An admin must create the user beforehand, password 123. This is obviously only
    a hack, and should be eventually replaced with a full registration suite.
    """
    if request.method == 'POST':
        # FIXME: can't find the damn user for some reason...
        user = User.objects.filter(username=request.POST.get('username')).first()
        if user and user.check_password('123'):
            user.set_password(request.POST.get('password', '123'))
            user.save()
    return views.login(request, template_name='oneall/nosocial.html')
