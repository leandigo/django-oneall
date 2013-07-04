class OAList(list):
    """
    A List of representing a JSON array with nested objects.
    """
    each = None

    def __init__(self, init_list=None):
        """
        A constructor which receives an iterable, and recursively converts all nested list and dict objects to
        OAList and OADict respectively. It also creates by_* methods allowing to perform grouping and search
        on OADict objects within the list.
        If subclass has the `each` attribute set to a class, all objects in list will be initialized as instances
        of that class.

        :param iterable init_list: Values to initiate list with.
        """
        if self.each:
            super(OAList, self).__init__([self.each(**item) for item in init_list])
        else:
            super(OAList, self).__init__([_convert_base(item) for item in init_list])

        self._dict_items = [item for item in self if isinstance(item, OADict)]

        for key in set().union(*[item.keys() for item in self._dict_items]):
            setattr(self, 'by_%s' % key, self._by_attr(key))

    def _by_attr(self, attr):
        """
        Create a custom by_attr function for grouping and searching
        """
        def by_attr(query=None, first=False):
            if query:
                ret = []
                for item in self._dict_items:
                    if item.get(attr) == query:
                        if first:
                            return item
                        ret.append(item)
                return ret

            else:
                ret = {}
                [ret.setdefault(item.get(attr), []).append(item) for item in self._dict_items
                    if not (isinstance(item.get(attr), OADict) or isinstance(item.get(attr), OAList))]
                return ret
        return by_attr

    def drop_nulls(self):
        while self.count(None):
            self.remove(None)
        [item.drop_nulls() for item in self if isinstance(item, OADict) or isinstance(item, OAList)]

class OADict(dict):
    """
    A JavaScript-object-like representing a JSON object with nested objects
    """
    ignored = ['response', 'oneall']

    def __init__(self, *args, **kwargs):
        super(OADict, self).__init__(
            *args,
            **dict((key, _convert_base(value)) for key, value in kwargs.iteritems())
        )
        [setattr(self, key, value) for key, value in self.iteritems()]
        self._populate()

    def __setattr__(self, key, value):
        super(OADict, self).__setattr__(key, value)
        if key not in self.ignored: super(OADict, self).__setitem__(key, value)

    def __setitem__(self, key, value):
        super(OADict, self).__setitem__(key, value)
        super(OADict, self).__setattr__(key, value)

    def _populate(self):
        pass

def _convert_base(item):
    return {
        dict : lambda: OADict(**item),
        list : lambda: OAList(item),
    }.get(type(item), lambda: item)()
