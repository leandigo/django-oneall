# -*- coding: utf-8 -*-
from logging import getLogger

from django.conf import settings
from django.contrib.auth import authenticate, login, logout, views
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse
from django.http.response import HttpResponseRedirectBase
from django.shortcuts import render, resolve_url
from django.views.decorators.csrf import csrf_exempt

from .forms import LoginForm
from .models import User, OneAllUserIdentity

log = getLogger(__name__)


class HttpResponseSeeOther(HttpResponseRedirectBase):
    status_code = 303


def redirect(to, *args, **kwargs):
    return HttpResponseSeeOther(resolve_url(to, *args, **kwargs))


@csrf_exempt
def oa_login(request: HttpRequest) -> HttpResponse:
    """
    Display and callback view for OneAll Authentication.
    """
    if request.user and request.user.is_authenticated():
        return redirect('oneall-profile')
    context = {
        'login_failed': False,
        'form': LoginForm(),
    }
    if request.method == 'POST':
        user = authenticate(**dict(request.POST.items()))
        if user:
            login(request, user)
            return redirect(request.GET.get('next') or settings.LOGIN_REDIRECT_URL)
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
        return redirect(url)
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
