from urllib2 import Request, urlopen
from base64 import encodestring
from json import dumps, loads
from base import OADict
from classes import Users, Connections, Connection, User

class OneAll():
    """
    A worker for the OneAll REST API.
    """
    DEFAULT_API_DOMAIN = 'https://{site_name}.api.oneall.com'
    FORMAT__JSON = 'json'

    bindings = {}

    def __init__(self, site_name, public_key, private_key, base_url=None):
        """
        :param str site_name: The name of the OneAll site
        :param str public_key: API public key for the site
        :param str private_key: API private key for the site
        :param str base_url: An alternate format for the API URL
        """
        self.base_url = base_url if base_url else OneAll.DEFAULT_API_DOMAIN.format(site_name=site_name)
        self.public_key = public_key
        self.private_key = private_key

    def _exec(self, action, params={}, post_params=None):
        """
        Execute an API action

        :param str action: The action to be performed. Translated to REST call
        :param str params: Additional GET parameters for action
        :post_params: POST parameters for action
        :returns dict: The JSON result of the call in a dictionary format
        """
        request_url = '%s/%s.%s' % (self.base_url, action, OneAll.FORMAT__JSON)
        for ix, (param, value) in enumerate(params.iteritems()):
            request_url += "%s%s=%s" % (('?' if ix == 0 else '&'), param, value)
        req = Request(request_url, dumps(post_params) if post_params else None, {'Content-Type': 'application/json'})
        auth = encodestring('%s:%s' % (self.public_key, self.private_key)).replace('\n', '')
        req.add_header('Authorization', 'Basic %s' % auth)
        return loads(urlopen(req).read())

    def _paginated(self, action, data, page_number=1, last_page=1, fetch_all=False, rtype=OADict):
        """
        Wrapper for paginated API calls. Constructs a response object consisting of one or more pages for paginated
        calls such as /users/ or /connections/. Returned object will have the ``pagination`` attribute equaling the
        the ``pagination`` value of the last page that was loaded.

        :param str action: The action to be performed.
        :param str data: The data attribute that holds the response payload
        :param int page_number: The first page number to load
        :param int last_page: The last page number to load
        :param bool fetch_all: Whether to fetch all records or not
        :param type rtype: The return type of the of the method
        :returns OADict: The API call result
        """
        oa_object = rtype()
        while page_number <= last_page or fetch_all:
            response = OADict(**self._exec(action, {'page' : page_number})).response
            page = getattr(response.result.data, data)
            oa_object.count = getattr(oa_object, 'count', 0) + getattr(page, 'count', 0)
            oa_object.entries = getattr(oa_object, 'entries', []) + getattr(page, 'entries', [])
            oa_object.pagination = page.pagination
            oa_object.response = response
            page_number += 1
            if page.pagination.current_page == page.pagination.total_pages:
                break
        return oa_object

    def users(self, page_number=1, last_page=1, fetch_all=False):
        """
        Get users

        :param int page_number: The first page number to load
        :param int last_page: The last page number to load
        :param bool fetch_all: Whether to fetch all records or not
        :returns Users: The users objects
        """
        users = self._paginated('users', 'users', page_number, last_page, fetch_all, Users)
        users.oneall = self
        [setattr(entry, 'oneall', self) for entry in users.entries]
        return users

    def user(self, user_token):
        """
        Get a user by user token

        :param str user_token: The user token
        :returns User: The user object
        """
        response = OADict(**self._exec('users/%s' % (user_token))).response
        user = User(**response.result.data.user)
        user.response = response
        user.oneall = self
        return user

    def user_contacts(self, user_token):
        """
        Get user's contacts by user token

        :param str user_token: The user token
        :returns OADict: User's contacts object
        """
        response = OADict(**self._exec('users/%s/contacts' % (user_token))).response
        user_contacts = OADict(**response.result.data.identities)
        user_contacts.response = response
        return user_contacts

    def connections(self, page_number=1, last_page=1, fetch_all=False):
        """
        Get connections

        :param int page_number: The first page number to load
        :param int last_page: The last page number to load
        :param bool fetch_all: Whether to fetch all records or not
        :returns Users: The connections
        """
        connections = self._paginated('connections', 'connections', page_number, last_page, fetch_all, rtype=Connections)
        connections.oneall = self
        [setattr(entry, 'oneall', self) for entry in connections.entries]
        return connections

    def connection(self, connection_token):
        """
        Get connection details by connection token

        :param str connection_token: The connection token
        :returns Connection: The requested connection
        """
        response = OADict(**self._exec('connection/%s' % (connection_token))).response
        connection = Connection(**response.result.data)
        connection.response = response
        return connection

    def user_contacts(self, user_token):
        """
        Get user's contacts

        :param str user_token: The user_token of the user whose contacts are to be fetched
        :returns OADict: The user's contacts
        """
        response = OADict(**self._exec('users/%s/contacts' % (user_token))).response
        contacts = OADict(**response.result.data.identities)
        contacts.response = response
        return contacts

    def publish(self, user_token, post_params):
        """
        Publish a message on behalf of the user

        :param str user_token: The user token
        :param dict post_params: The message in the format described in OneAll documentation
        :returns OADict: The API response
        """
        return OADict(**self._exec('users/%s/publish' % user_token, post_params=post_params))
