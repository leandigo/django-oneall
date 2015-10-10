.. coding: utf-8

Configuration
`````````````

This guide assumes you already have a `Django project`_ and that all your applications use the recommended Django
methods for enforcing authentication, such as the |lr|_ decorator.

It also assumes that you have already created your OneAll site named ``mysite``, with public and private keys, and that
you have already used the `OneAll control panel`_ to set up at least one initial social network for login.

``settings.py``
^^^^^^^^^^^^^^^

First, add ``django_oneall`` to ``INSTALLED_APPS``, make sure you have ``django.contrib.auth`` before it::

    INSTALLED_APPS = (
        'django.contrib.auth',
        'django_oneall',
        # (…)
    )

Second, add the Django authentication backends::

    AUTHENTICATION_BACKENDS = (
        'django_oneall.auth.OneAllAuthBackend',
        'django_oneall.auth.EmailTokenAuthBackend',  # Optional
    )

Third, add the OneAll settings. Here's a minimal set-up::

    ONEALL = {
        'credentials': {
            'site_name': 'mysite',
            'public_key': '2d27cffd-xxxx-xxxx-xxxx-xxxxxxxxxxxx',
            'private_key': '84d94998-xxxx-xxxx-xxxx-xxxxxxxxxxxx',
        },
    }

Here's a different, more detailed alternative to the third step::

    ONEALL = {
        'credentials': {
            'site_name': 'mysite',
            'public_key': '2d27cffd-xxxx-xxxx-xxxx-xxxxxxxxxxxx',
            'private_key': '84d94998-xxxx-xxxx-xxxx-xxxxxxxxxxxx',
        },
        'login_widget': {
            'providers': ['amazon', 'blogger', 'disqus', 'draugiem', 'facebook',
                          'foursquare', 'github', 'google', 'instagram', 'linkedin',
                          'livejournal', 'mailru', 'odnoklassniki', 'openid',
                          'paypal', 'reddit', 'skyrock', 'stackexchange', 'steam',
                          'twitch', 'twitter', 'vimeo', 'vkontakte', 'windowslive',
                          'wordpress', 'yahoo', 'youtube'],
            'grid_sizes': [7, 5],
            # Any setting allowed in the login widget assistant can be put here.
        },
        'store_user_info': True,
        'email_token_expiration_hours': 3,
    }

If you plan to use E-mail Token authentication, you must also `configure your e-mail backend`_.
Here's a good setting for development::

    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

Update Database
^^^^^^^^^^^^^^^

As with any Django app install::

    manage.py migrate

After that, if you're updating from 0.1.4 or older, the legacy table ``oneall_cache`` is ignored since 0.2
(September 2015). In order to import users from the old to the new table, you need to also run::

    manage.py legacyimport

``urls.py``
^^^^^^^^^^^
Add the following URL pattern to your ``urlpatterns`` in your global ``urls.py``::

    url(r'^accounts/', include('django_oneall.urls')),

Using this Django App in ``/accounts/`` will work as a drop-in replacement to ``django.contrib.auth``.

However, if you're using ``django.contrib.admin``, it implements its own login screen, which conflicts with OneAll's.
You then need to override its login screen like so::

    url(r'^admin/login', 'django_oneall.views.oa_login'),
    url(r'^admin/', include(admin.site.urls)),

Super User
^^^^^^^^^^

The super user command is::

    python manage.py setsuperuser [user]

Where ``[user]`` can be either of:

#. OneAll Token (a UUID).
#. Django user Id (an integer; see your ``auth_user`` table for a list).
#. An e-mail address.

For OneAll Token or Django user Id, your user must already exist and they will be promoted.

For e-mail authentication, the user will be created if necessary and will be promoted regardless.
The console will display the e-mail login link to be manually pasted in a web browser.
Should your end user be unavailable to complete login, don't worry, they have already been made super-user.

Template
^^^^^^^^
Pages that implement OneAll widgets must include in their ``<head>``::

    {% load oneall %}
    {% oneall_header %}

The login Widget can be included manually as instructed through the OneAll assistant, or, if you're feeling lazy::

    {% oneall_social_login %}

You can also pass an optional argument (it must be the Django ``User`` object) if you want social linking instead::

    {% oneall_social_login current_user %}

This is all auto provided by the included templates ``login.html`` and ``profile.html``.
It is recommended to use them as a base to make your own login and profile pages.

.. _Django project: https://docs.djangoproject.com/en/1.8/intro/tutorial01/
.. |lr| replace:: ``login_required``
.. _lr: https://docs.djangoproject.com/en/1.8/topics/auth/default/#django.contrib.auth.decorators.login_required
.. _OneAll control panel: https://app.oneall.com/applications/
.. _configure your e-mail backend: https://docs.djangoproject.com/en/1.8/ref/settings/#email-backend
