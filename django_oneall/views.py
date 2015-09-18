# -*- coding: utf-8 -*-
from logging import getLogger
from threading import Thread

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.exceptions import SuspiciousOperation
from django.core.mail import EmailMessage
from django.core.urlresolvers import reverse
from django.http.response import HttpResponseRedirectBase
from django.middleware.csrf import CsrfViewMiddleware
from django.shortcuts import render, resolve_url
from django.utils.translation import ugettext_lazy as _t, ugettext as _tt
from django.views.decorators.csrf import csrf_exempt

from .app import settings
from .auth import OneAllAuthBackend, EmailTokenAuthBackend
from .forms import EmailForm
from .models import SocialUserCache

log = getLogger(__name__)


class HttpResponseSeeOther(HttpResponseRedirectBase):
    status_code = 303


def redirect(to, *args, **kwargs):
    return HttpResponseSeeOther(resolve_url(to, *args, **kwargs))


@csrf_exempt
def oa_login(request, noise=''):
    """ Display and callback view for OneAll Authentication. """
    if request.user and request.user.is_authenticated():
        return redirect('oneall-profile')
    auth_with = None
    context = {
        'login_failed': False,
        'check_your_mail': False,
        'logged_out': 'logout' in noise,
        'email_form': EmailForm(),
    }
    if OneAllAuthBackend.KEY in request.POST:
        auth_with = dict(request.POST.items())
    elif 'email' in request.POST:
        csrf_check(request)  # maybe not relevant
        email = request.POST['email']
        args = EmailTokenAuthBackend().issue(email)
        mail_login_token(request, email, args)
        context['check_your_mail'] = True
    elif EmailTokenAuthBackend.KEY in request.GET:
        auth_with = dict(request.GET.items())
    if auth_with:
        user = authenticate(**auth_with)
        if user:
            login(request, user)
            return redirect(request.GET.get('next') or settings.default_url)
        else:
            context['login_failed'] = True
    return render(request, 'oneall/login.html', context)


def mail_login_token(request, email, args):
    args.setlist('next', request.GET.getlist('next'))
    relative_uri = '%s?%s' % (reverse('oneall-login'), args.urlencode())
    message = EmailMessage()
    message.subject = _t("Login")
    message.to = [email]
    message.body = "\n".join([
        _tt("Complete your login using this link:"),
        request.build_absolute_uri(relative_uri),
    ])
    Thread(target=message.send, args=(True,)).start()


def oa_logout(request):
    """ Logs out the user and then takes them somewhere else. """
    logout(request)
    url = request.GET.get('next')
    if url:
        return redirect(url)
    else:
        return redirect('oneall-login', '_from_logout')


@login_required
@csrf_exempt
def oa_profile(request):
    """ Displays current user profile, allows updates and social linkings. """
    context = {
        'user': request.user,
        'identity': SocialUserCache.objects.filter(user=request.user).first(),
        'form': EmailForm({'email': request.user.email})
    }
    if 'connection_token' in request.POST:
        OneAllAuthBackend(request.user).authenticate(**request.POST)
    elif 'email' in request.POST and request.user.email != request.POST['email']:
        csrf_check(request)
        EmailTokenAuthBackend(request.user).issue(request.POST['email'])
    return render(request, 'oneall/profile.html', context)


def csrf_check(request, raise_exception=True):
    problem = CsrfViewMiddleware().process_view(request, None, (), {})
    if problem and raise_exception:
        raise SuspiciousOperation
    else:
        return not problem
