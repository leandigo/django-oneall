from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login
from django.conf import settings
from django.http import HttpResponseRedirect

@csrf_exempt
def oneall_auth(request):
    """
    Callback view for OneAll Authentication
    :returns HttpResponseRedirect: A redirection to the LOGIN_REDIRECT_URL
    """
    connection_token=request.POST['connection_token']
    user = authenticate(token=connection_token)
    login(request, user)
    return HttpResponseRedirect(settings.LOGIN_REDIRECT_URL)
