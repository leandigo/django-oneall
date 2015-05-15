# -*- coding: utf-8 -*-
from django.conf import settings
from django.shortcuts import redirect, render
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login
from django.http import HttpRequest, HttpResponse


@csrf_exempt
def oneall_auth(request: HttpRequest) -> HttpResponse:
    """
    Display and callback view for OneAll Authentication.
    """
    if request.method == 'POST':
        connection_token = request.POST['connection_token']
        user = authenticate(token=connection_token)
        if user:
            login(request, user)
            return redirect(request.GET.get('next') or '/')
    context = {'oa_site_name': settings.ONEALL_SITE_NAME}
    return render(request, 'oneall/login.html', context)
