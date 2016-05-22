.. coding: utf-8

django-oneall - Django Authentication support for OneAll
========================================================

..  image:: https://badges.gitter.im/Join%20Chat.svg
    :alt: Join the chat at https://gitter.im/leandigo/django-oneall
    :target: https://gitter.im/leandigo/django-oneall?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge
..  image:: https://readthedocs.org/projects/pip/badge/
    :alt: Read the documentation at http://django-oneall.readthedocs.io/
    :target: http://django-oneall.readthedocs.io/?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge

**OneAll** (|oneall|_) provides web-applications with a unified API for **30+ social networks**.

**django-oneall** is a Django app providing allowing user authentication and management through OneAll

Requirements:

#. django_
#. pyoneall_

This package provides user authentication capabilities based on ``django.contrib.auth``. It provides the following
components:

#. Authentication Backend
#. An identity model which stores a cached copy of the user's identity
#. A callback view for the authentication process

Installation::

    pip install django_oneall

See the `full documentation`_ for configuration.

License
-------
Copyright (c) 2013-2015, Leandigo (|leandigo|_) and Ekevoo_.

Released under the MIT License. See the LICENSE_ file for details.

.. |oneall| replace:: http://www.oneall.com
.. _oneall: http://www.oneall.com
.. _django: https://www.djangoproject.com
.. _pyoneall: https://github.com/leandigo/pyoneall
.. _full documentation: http://django-oneall.readthedocs.io/
.. |leandigo| replace:: www.leandigo.com
.. _leandigo: http://www.leandigo.com
.. _Ekevoo: http://ekevoo.com
.. _LICENSE: LICENSE.rst
