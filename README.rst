WARNING!
========
WARNING!!
---------
WARNING!!!
``````````

**This is the Django documentation from before the fork.**

**A LOT HAS CHANGED.**

**Feel free to file a documentation ticket if you're frustrated.**
**I'll come and fix it right then.**
**Right now I'm still focusing on my changes.**


django-oneall - Django Authentication support for OneAll
========================================================

**OneAll** (|oneall|_) provides web-applications with a unified API for **20+ social networks**.

**django-oneall** is a Django app providing allowing user authentication and management through OneAll

Disclaimer
----------
*This package is new, and so far has been tested in a development of a small number of projects.*
*Please be sure to test all edge-cases where this package is used with your application!*

Requirements
------------

#. ``django>=1.4`` (Wasn't tested on earlier versions, but might work)
#. ``pyoneall==0.1``

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

Add the authentication backend::

    AUTHENTICATION_BACKENDS = ('django_oneall.auth.OneAllAuthBackend',)

Configure OneAll connection::

    ONEALL_SITE_NAME = 'NAME OF YOUR ONEALL SITE'
    ONEALL_PRIVATE_KEY = 'PRIVATE KEY OF YOUR SITE'
    ONEALL_PUBLIC_KEY = 'PUBLIC KEY OF YOUR SITE'

Configure behavior (these are good to go as they are here, so you can just copy-paste)::

    # This setting lets you decide which identity data you want stored in the User model.
    # The keys stand for the fields in the User model, while the values are the expressions that will be evaluated
    # as attributes of the identity object as received from OneAll. There can be more than one identity expression,
    # in case different authentication providers have different data structures.
    # Note that the usernames will default to the user_token, which is a UUID. You can override it with any other
    # unique identity information
    ONEALL_CACHE_FIELDS = {
        'username': ('user_token',),
        'email': ('emails[0].value',),
        'first_name': ('name.givenName',),
        'last_name': ('name.familyName',),
    }

    # User identity is always cached on first authentication. However, if you want to spare an API call for users
    # who are already known to your Django app, you can disable the refresh of cache for the second time they
    # connect and onward.
    ONEALL_REFRESH_CACHE_ON_AUTH = True

    # The OneAll cache table in the DB, where cached identities are stored
    ONEALL_CACHE_TABLE = 'oneall_cache'

``urls.py``
^^^^^^^^^^^
Add the following URL pattern to your ``urlpatterns`` tuple::

    url(r'^oneall/', include('django_oneall.urls'))

This should enable you to use the callback view at ``/oneall/auth/``

Template
^^^^^^^^
When embedding the body of the OneAll plugin inside your login template, set the ``callback_uri`` attribute to the URL
of the OneAll callback view like so: ``http://example.com{% url oneall_auth %}``. The template might look like::

    <script type="text/javascript">
        oneall.api.plugins.social_login.build("social_login_container", {
            'providers' :  ['facebook', 'google', 'linkedin', 'twitter', 'yahoo'],
            'css_theme_uri': 'https://oneallcdn.com/css/api/socialize/themes/buildin/connect/large-v1.css',
            'grid_size_x': '1',
            'callback_uri': 'http://example.com{% url oneall_auth %}'
        });
    </script>

Notes and Stuff
---------------
After configuring, ``python manage.py syncdb`` is **required**.

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
``AUTHENTICATION_BACKENDS``. You can find docs on that at `Connection API Documentation`_, or take a look at the very
simple code in ``views.py`` provided in this package.

License
-------
Copyright (c) 2013, Leandigo (|leandigo|_)

Released under the MIT License. See the LICENSE file for details.

.. |oneall| replace:: http://www.oneall.com
.. _oneall: http://www.oneall.com
.. |onealldoc| replace:: http://docs.oneall.com
.. _onealldoc: http://docs.oneall.com
.. _Connection API Documentation: http://docs.oneall.com/api/resources/connections/
.. |leandigo| replace:: www.leandigo.com
.. _leandigo: http://www.leandigo.com
