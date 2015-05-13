from django.conf.urls import patterns, url

urlpatterns = patterns(
    '',  # why is this necessary?
    url(r'^auth/$', 'django_oneall.views.oneall_auth', name='oneall_auth'),
)
