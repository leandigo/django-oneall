# -*- coding: utf-8 -*-
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login, logout
from django.http import HttpRequest, HttpResponse

from .models import OneAllUserIdentity


@csrf_exempt
def oa_login(request: HttpRequest) -> HttpResponse:
    """
    Display and callback view for OneAll Authentication.
    """
    if request.method == 'POST':
        connection_token = request.POST['connection_token']
        user = authenticate(token=connection_token)
        if user:
            login(request, user)
            return redirect(request.GET.get('next') or settings.LOGIN_REDIRECT_URL)
    context = {'oa_site_name': settings.ONEALL_SITE_NAME}
    return render(request, 'oneall/login.html', context)


def oa_logout(request: HttpRequest) -> HttpResponse:
    """
    Logs out the user and takes them somewhere if requested.
    """
    logout(request)
    url = request.GET.get('next')
    return redirect(url) if url else render(request, 'oneall/logout.html')


@login_required
def oa_profile(request: HttpRequest) -> HttpResponse:
    context = {
        'user': request.user,
        'identity': OneAllUserIdentity.objects.filter(user=request.user).first(),
    }
    return render(request, 'oneall/profile.html', context)
