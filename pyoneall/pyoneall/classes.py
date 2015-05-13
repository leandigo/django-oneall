from base import OAList, OADict

class Users(OADict):
    """
    Represents a /users/ OneAll API call
    """
    class UsersEntries(OAList):
        """
        Represents the `entries` attribute
        """
        class UsersEntry(OADict):
            """
            Represents each object within `entries`
            """
            pass

            def user(self):
                """
                Returns full user data for user_token in entry
                """
                if self.oneall:
                    return self.oneall.user(self.user_token)

        each = UsersEntry

    @property
    def entries(self):
        return getattr(self, '_entries', [])

    @entries.setter
    def entries(self, value):
        self._entries = Users.UsersEntries(value)

class Connections(OADict):
    """
    Represents the /connections/ OneAll API call
    """

    class ConnectionsEntries(OAList):
        """
        Represents the `entries` attribute
        """

        class ConnectionsEntry(OADict):
            """
            Represents each object within `entries`
            """

            def connection(self):
                """
                Returns full connection data for connection_token in entry
                """
                if self.oneall:
                    return self.oneall.connection(self.connection_token)

        each = ConnectionsEntry

    @property
    def entries(self):
        return getattr(self, '_entries', [])

    @entries.setter
    def entries(self, value):
        self._entries = Connections.ConnectionsEntries(value)

class Connection(OADict):
    """
    A OneAll Connection
    """
    pass

class User(OADict):
    """
    A OneAll User
    """
    def contacts(self):
        """
        Retrieve user's contacts
        """
        if self.oneall:
            return self.oneall.user_contacts(self.user_token)