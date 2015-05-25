python3-oneall
==============

Authentication with 20+ social networks using OneAll_, with Django_ support.

This is a fork of `leandigo/django-oneall`_ with the following changes:

- **Python 3!** The modules I've forked from are Python 2 only.
  I could've just futurized instead, but I find it pollutes the code too much,
  and I actually want to help motivating the switch away from Py2.
- **Merged requisite OneAll support into the module,**
  leaving Django support as an optional component of the module.
  Support frameworks other than Django can be added in the same way.
  This is inspired by the architecture of `python-social-auth`_.
- **New views,** compatible with ``django.contrib.auth``, for ease of integration.
  This is very much in flux, but final goal is adding an ``'^accounts/'`` URL route,
  putting settings in, and done.

.. _OneAll: https://oneall.com/
.. _Django: https://www.djangoproject.com/
.. _leandigo/django-oneall: https://github.com/leandigo/django-oneall
.. _python-social-auth: https://github.com/omab/python-social-auth/


Further documentation
---------------------

- For the `pure Python part of the module`_
- And for the `Django part of the module`_

.. _pure Python part of the module: core.rst
.. _Django part of the module: django.rst


Roadmap
-------

- Single login page with social network optional
  and actually asking the visitor for their username.
- Easy to use OneAll login widget for use in global templates.
- Implement OneAll social link. Seems like a breeze.
- Implement OneAll link sharing. I have no idea where to start.


Sample Django settings
----------------------

.. code-block:: python

    ONEALL_SITE_NAME = 'py3tests'
    ONEALL_PUBLIC_KEY = 'bf3a6a88-...'
    ONEALL_PRIVATE_KEY = '35fc1a5e-...'
    ONEALL_LOGIN_WIDGET = {
        'providers': ['amazon', 'blogger', 'disqus', 'draugiem', 'facebook',
                      'foursquare', 'github', 'google', 'instagram', 'linkedin',
                      'livejournal', 'mailru', 'odnoklassniki', 'openid',
                      'paypal', 'reddit', 'skyrock', 'stackexchange', 'steam',
                      'twitch', 'twitter', 'vimeo', 'vkontakte', 'windowslive',
                      'wordpress', 'yahoo', 'youtube'],
        'grid_sizes': [7, 5],
    }
