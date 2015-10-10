.. coding: utf-8

django-oneall
=============

This package is a Django_ application that provides drop-in social authentication support using OneAll_.

Use this package's auth modules to provide authentication. New users are automatically created, and you can set
authorization through the admin interface of ``django.contrib.auth``. Then you can use the ``url`` subpackage as your
``/accounts`` route, Django automatically uses it for any other application that requires login for any of its views.

OneAll_ provides a unified API for 30+ social networks. A big part of the benefit is that their control panel walks you
through the step of creating and obtaining the appropriate tokens for each of them, which is a very convoluted process
for the more popular social networks. After doing that, the only change you need to make to your application is adding
the new network to your list of supported networks; all the rest is transparent.

Installation
------------

Install it using the CheeseShop_::

    pip install django_oneall

This will also install its requirements Django_ and pyoneall_, and whichever the requirements of those are.
After that you must configure your Django project to use ``django-oneall``.

.. _Django: https://www.djangoproject.com/
.. _OneAll: https://www.oneall.com/
.. _pyoneall: https://pypi.python.org/pypi/pyoneall
.. _CheeseShop: https://pypi.python.org/pypi
