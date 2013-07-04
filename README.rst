pyoneall - OneAll API Wrapper
=============================

**OneAll** (|oneall|_) provides web-applications with a unified API for **20+ social networks**.
**pyoneall** provides developers with OneAll accounts a simple interface with the OneAll API for Python-based web-applications.

Disclaimer
----------
*This package is new, and so far has been tested in a development of a small number of projects.*
*Please be sure to test all edge-cases where this package is used with your application!*

Implementation Overview
-----------------------
OneAll API documentation is available at |onealldoc|_. However, in order to use pyoneall with your application, it's
enough to read the docs for the Connection API: `Connection API Documentation`_.

So far, we have tested pyoneall within Flask and Django apps. To use OneAll as a Django authentication backend,
please check out our ``django_oneall`` project, which relies on this package.

pyoneall defines the ``OneAll`` class, which is the API client. As of now, it has the following methods:

:``connections()``: Get a list of social connections to the site
:``connection()``: Get detailed connection data including user details
:``users()``: Get a list of users that have connected with the site
:``user()``: Get detailed user data
:``user_contacts()``: Get a list of user's contacts
:``publish()``: Publish a message using user's social network account

As pyoneall wraps a REST API which returns JSON objects, the objects returned by the methods behave in a somewhat
JavaScript-like manner. This means that in addition to the ``dict``-style ``object['key']`` notation, you can also
use ``object.key``.

Also, arrays nested in the JSON responses, are represented by a class that defines a ``by_*()`` grouping and searching
method in an addition to the ``list`` methods it inherits from.

For more information on these classes, check out ``help(pyoneall.base.OADict)`` and ``help(pyoneall.base.OAList)``.

Example
-------

Authentication
~~~~~~~~~~~~~~
Access to the OneAll API requires authentication. Obtain your API credentials following the procedure described at
`Authentication Documentation`_.

Create an instance of the OneAll client::

    from pyoneall import OneAll

    oa = OneAll(
        site_name='NAME OF YOUR ONEALL SITE',
        public_key='PUBLIC KEY OF YOUR SITE',
        private_key='PRIVATE KEY OF YOUR SITE'
    )

The Connection API
~~~~~~~~~~~~~~~~~~
Fetching connections lists
**************************
::

    connections = oa.connections()

``connections`` now contains the "connections" portion of the result of the API call, as described in
`<http://docs.oneall.com/api/resources/connections/list-all-connections/>`_.
Full response data (for debugging and whatnot) is in ``connections.response``.

OneAll uses pagination for calls which contain many entries. Each call returns a page up to 500 entries. When the
``OneAll.connections()`` method is executed without arguments, only the first page is loaded. You the access the
pagination information in ``connections.pagination``.

In order to load a custom range of pages, you can do something like::

    connections = oa.connections(first_page=3, last_page=6)

Or, if you want to load all pages, use::

    connections = oa.connections(fetch_all=True)

Of course, this will result in multiple API calls.

The connections list itself is in ``connections.entries``::

    >>> connections.entries
    [{u'callback_uri': u'http://www.example.com/connect/',
     u'connection_token': u'cf2fffc7-34dc-484e-95cd-13f8ab838e22',
     u'date_creation': u'Sun, 23 Jun 2013 14:12:43 +0200',
     u'status': u'succeeded'},
    {u'callback_uri': u'http://m.example.com/connect/',
     u'connection_token': u'4276bd23-3605-4679-acd2-963148c477cc',
     u'date_creation': u'Sun, 23 Jun 2013 14:13:20 +0200',
     u'status': u'succeeded'},
    {u'callback_uri': u'http://www.example.com/connect/',
     u'connection_token': u'58ad2a04-ed1e-4799-a3ca-2b26651e35a0',
     u'date_creation': u'Sun, 23 Jun 2013 14:18:00 +0200',
     u'status': u'succeeded'},
    {u'callback_uri': u'http://m.example.com/connect/',
     u'connection_token': u'e5231790-c6dc-4ce8-9922-792a2aebbba2',
     u'date_creation': u'Sun, 23 Jun 2013 14:18:11 +0200',
     u'status': u'succeeded'},
    {u'callback_uri': u'http://www.example.com/connect/',
     u'connection_token': u'f82ad1e5-113f-46a2-b1c5-2a57a6002401',
     u'date_creation': u'Sun, 23 Jun 2013 14:21:14 +0200',
     u'status': u'succeeded'}]

In the example above, you can see that some connections were made with the callback of the desktop website
(``http://www.example.com/connect/``), and some were made with the mobile webapp (``http://m.example.com/connect/``).
We can get an object grouped by the "callback_uri" using::

    >>> connections.entries.by_callback_uri()
    {u'http://www.example.com/connect/': [
        {u'callback_uri': u'http://www.example.com/connect/',
         u'connection_token': u'cf2fffc7-34dc-484e-95cd-13f8ab838e22',
         u'date_creation': u'Sun, 23 Jun 2013 14:12:43 +0200',
         u'status': u'succeeded'},
        {u'callback_uri': u'http://www.example.com/connect/',
         u'connection_token': u'58ad2a04-ed1e-4799-a3ca-2b26651e35a0',
         u'date_creation': u'Sun, 23 Jun 2013 14:18:00 +0200',
         u'status': u'succeeded'}],
        {u'callback_uri': u'http://www.example.com/connect/',
         u'connection_token': u'f82ad1e5-113f-46a2-b1c5-2a57a6002401',
         u'date_creation': u'Sun, 23 Jun 2013 14:21:14 +0200',
         u'status': u'succeeded'},
     u'http://m.example.com/connect/': [
        {u'callback_uri': u'http://m.example.com/connect/',
         u'connection_token': u'4276bd23-3605-4679-acd2-963148c477cc',
         u'date_creation': u'Sun, 23 Jun 2013 14:13:20 +0200',
         u'status': u'succeeded'},
        {u'callback_uri': u'http://m.example.com/connect/',
         u'connection_token': u'e5231790-c6dc-4ce8-9922-792a2aebbba2',
         u'date_creation': u'Sun, 23 Jun 2013 14:18:11 +0200',
         u'status': u'succeeded'}]}

Or get a list of connections with a specific "callback_uri"::

    >>> connections.entries.by_callback_uri('http://m.example.com/connect/')
    [{u'callback_uri': u'http://m.example.com/connect/',
     u'connection_token': u'4276bd23-3605-4679-acd2-963148c477cc',
     u'date_creation': u'Sun, 23 Jun 2013 14:13:20 +0200',
     u'status': u'succeeded'},
    {u'callback_uri': u'http://m.example.com/connect/',
     u'connection_token': u'e5231790-c6dc-4ce8-9922-792a2aebbba2',
     u'date_creation': u'Sun, 23 Jun 2013 14:18:11 +0200',
     u'status': u'succeeded'}]

Reading connection details
**************************
In order to get the **user_token** and the user's social identity you can pass a **connection_token** to the
``connection()`` method of the ``OneAll`` instance::

    some_connection = oa.connection('e5231790-c6dc-4ce8-9922-792a2aebbba2')

Or, alternatively you can fetch the connection details through the ``connection()`` method of an entry in the list
of connections::

    some_connection = connections.entries[3].connection()

``some_connection`` will now contain the "connection" portion of the response described in the API documentation for
`Read Connection Details`_, most importantly ``some_connection.user`` and ``some_connection.user.user_token``

The User API
~~~~~~~~~~~~
Fetching user list
******************
``OneAll.users()`` behaves the same way ``OneAll.connections()`` does, arguments and all. This is due to the similarity
of the List Users and the List Connections API, in terms of pagination and entries structure.
::

    users = oa.users()

Now, you can access ``users.entries``, or even access detailed user data with ``users.entries[4].user()``.

Reading user details
********************
Read user details using::

    user_token = some_connection.user.user_token
    some_user = oa.user(user_token)

``some_user`` will contain the "user" portion of the response detailed at
`<http://docs.oneall.com/api/resources/users/read-user-details/>`_.

Reading user's contacts
***********************
You can get the user's contacts (depending on the social network) with::

    contacts = some_user.contacts()

or, with::

    contacts = oa.user_contacts(user_token)

Publishing content on user's behalf
***********************************
First, you need to format a message as described at `<http://docs.oneall.com/api/resources/users/write-to-users-wall/>`_.
Afterwards, publish it using ``publish()``::

    message = {
        'request': {
            'message': {
                'parts': {
                    'text': {
                        'body': 'Hello World!' }}}}}

    oa.publish(user_token, message)

License
-------
Copyright (c) 2013, Leandigo (|leandigo|_)
Released under the MIT License. See the LICENSE file for details.

.. |leandigo| replace:: www.leandigo.com
.. _leandigo: http://www.leandigo.com
.. |oneall| replace:: http://www.oneall.com
.. _oneall: http://www.oneall.com
.. |onealldoc| replace:: http://docs.oneall.com
.. _onealldoc: http://docs.oneall.com
.. _Connection API Documentation: http://docs.oneall.com/api/resources/connections/
.. _Authentication Documentation: http://docs.oneall.com/api/basic/authentication/
.. _Read Connection Details: http://docs.oneall.com/api/resources/connections/read-connection-details/