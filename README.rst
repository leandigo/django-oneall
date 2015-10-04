django-oneall - Django Authentication support for OneAll
========================================================

.. image:: https://badges.gitter.im/Join%20Chat.svg
   :alt: Join the chat at https://gitter.im/leandigo/django-oneall
   :target: https://gitter.im/leandigo/django-oneall?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge

**OneAll** (|oneall|_) provides web-applications with a unified API for **30+ social networks**.

**django-oneall** is a Django app providing allowing user authentication and management through OneAll

Requirements
------------

#. ``django>=1.8`` (Wasn't tested on earlier versions, but might work)
#. ``pyoneall>=0.2.3``

Implementation Overview
-----------------------
OneAll API documentation is available at |onealldoc|_. However, in order to use pyoneall with your application, it's
enough to read the docs for the Connection API: `Connection API Documentation`_.

For more information on ``pyoneall`` the OneAll API wrapper that this package relies on, check out
`<https://github.com/leandigo/pyoneall>`_. It has more goodies you could use.

This package provides user authentication capabilities based on ``django.contrib.auth``. It provides the following
components:

#. Authentication Backend
#. An identity model which stores a cached copy of the user's identity
#. A callback view for the authentication process

Setup
-----

Installation
````````````
Add this app to your project directory, or install via::

    pip install django_oneall

Configuration
`````````````

``settings.py``
^^^^^^^^^^^^^^^

Add ``django_oneall`` to ``INSTALLED_APPS``, make sure you have ``django.contrib.auth`` enabled::

    INSTALLED_APPS = (
        'django.contrib.auth',
        # . . .
        'django_oneall',
    )

Add the Django authentication backends::

    AUTHENTICATION_BACKENDS = (
        'django_oneall.auth.OneAllAuthBackend',
        'django_oneall.auth.EmailTokenAuthBackend',  # Optional
    )

Configure OneAll, for example::

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

Credentials are mandatory. All other settings are optional.

If you plan to use E-mail Token authentication, you must also `configure your e-mail backend`_.
Here's a good setting for development::

    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

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

* You can promote an existing user to super user (OneAll Token, integer Django user ID, or user e-mail).
* You can create a new user that's super right from the start, with their e-mail.

Just run::

    python manage.py setsuperuser [user]

Whereas ``[user]`` can be either of the three.

Beware that this command **will never send any e-mail**;
it merely displays the e-mail login link to be manually pasted in your web browser.
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

Notes and Stuff
---------------
After configuring, ``python manage.py migrate`` is **required**.

If you're upgrading from ``django-oneall<1.0``, you must also run ``python manage.py legacyimport`` afterwards.

Now users can authenticate and attain user privileges using their social accounts, without the need for you app to
handle the registration.

Inside your views or any other Python code, you can access the user's identity information like this::

    user = User.objects.get(username='<user_token>')
    identity = user.identity

``identity`` is an instance of the ``OneAllUserIdentity`` model, which allows you access to cached user identity
information, provided by the social network the user used to authenticate. The data provided varies between different
social networks. ``vars(identity)`` will show you the user's information.

You can create your own authentication views. ``django.contrib.auth.authenticate`` and ``django.contrib.auth.login``
will work seamlessly with OneAll if you've added ``django_oneall.auth.OneAllAuthBackend`` to your
``AUTHENTICATION_BACKENDS``. You can find docs on that at `Connection API Documentation`_, or take a look at the
code in ``views.py`` provided in this package.

Roadmap
-------

- Internationalization.
- Implement `OneAll Social Link`_.

License
-------
Copyright (c) 2013-2015, Leandigo (|leandigo|_) and Ekevoo_.

Released under the MIT License. See the LICENSE file for details.

.. |oneall| replace:: http://www.oneall.com
.. _oneall: http://www.oneall.com
.. |onealldoc| replace:: http://docs.oneall.com
.. _onealldoc: http://docs.oneall.com
.. _Connection API Documentation: http://docs.oneall.com/api/resources/connections/
.. _configure your e-mail backend: https://docs.djangoproject.com/en/1.8/ref/settings/#email-backend
.. _OneAll Social Link: https://www.oneall.com/services/social-link/
.. |leandigo| replace:: www.leandigo.com
.. _leandigo: http://www.leandigo.com
.. _Ekevoo: http://ekevoo.com
