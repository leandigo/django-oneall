# -*- coding: utf-8 -*-
from logging import getLogger

from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse
from django.http.response import HttpResponseRedirectBase
from django.shortcuts import render, resolve_url
from django.views.decorators.csrf import csrf_exempt

from .auth import OneAllAuthBackend
from .forms import LoginForm, RegisterForm, UserProfileForm
from .models import SocialUserCache

log = getLogger(__name__)


class HttpResponseSeeOther(HttpResponseRedirectBase):
    status_code = 303


def redirect(to, *args, **kwargs):
    return HttpResponseSeeOther(resolve_url(to, *args, **kwargs))


@csrf_exempt
def oa_login(request: HttpRequest, noise='') -> HttpResponse:
    """ Display and callback view for OneAll Authentication. """
    if request.user and request.user.is_authenticated():
        return redirect('oneall-profile')
    context = {
        'login_failed': False,
        'logged_out': 'logout' in noise,
        'login_form': LoginForm(),
        'register_form': RegisterForm(),
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
    """ Logs out the user and then takes them somewhere else. """
    logout(request)
    url = request.GET.get('next')
    if url:
        return redirect(url)
    else:
        return redirect('oneall-login', '_from_logout')


@login_required
def oa_profile(request: HttpRequest) -> HttpResponse:
    """ Displays current user profile, allows updates and social linkings. """
    context = {
        'user': request.user,
        'identity': SocialUserCache.objects.filter(user=request.user).first(),
        'form': UserProfileForm(request.POST or None),
    }
    if request.POST:
        if 'connection_token' in request.POST:
            OneAllAuthBackend(request.user).authenticate(**request.POST)
    return render(request, 'oneall/profile.html', context)
