from model.update_type import UpdateType


class ObservableList(object):
    """
    Detects changes in list.

    In append, in remove and in setter, the `observer` is callable with changes
    details

    Based in https://www.pythonsheets.com/notes/python-basic.html#emulating-a-list
    """

    def __init__(self, lista=None):
        self._list = lista if lista is not None else []
        self.observer = lambda *args: ...

    def __str__(self):
        return repr(self._list)

    def append(self, item):
        """
        View `append` :class:`list` method

        Calls observer `self.observer(UpdateType.CREATED, item, index)` where
        _index_ is _item position_
        """
        self._list.append(item)
        self.observer(UpdateType.CREATED, item, len(self._list)-1)

    def remove(self, item):
        """
        View `remove` :class:`list` method

        Calls observer `self.observer(UpdateType.DELETED, item, index)` where _index_ is
        _item position_
        """
        index = self.index(item)
        self._list.remove(item)
        self.observer(UpdateType.DELETED, item, index)

    def index(self, x):
        return self._list.index(x)

    def insert(self, index, x):
        """
        View `insert` :class:`list` method

        Calls observer `self.observer(UpdateType.CREATED, item, index)`
        """
        self._list.insert(index, x)
        self.observer(UpdateType.CREATED, x, index)

    def __len__(self):
        return len(self._list)

    def __getitem__(self, index):
        return self._list[index]

    def __setitem__(self, index, val):
        """
        View `__setitem__` :class:`list` method

        Calls observer `self.observer(UpdateType.UPDATED, item, index)`
        if `val != self[index]`
        """
        if val == self[index]:
            return

        self._list[index] = val
        self.observer(UpdateType.UPDATED, val, index)

    def __delitem__(self, sliced):
        """
        View `__delitem__` :class:`list` method

        Calls observer `self.observer(UpdateType.DELETED, item, index)`
        where _item_ is `self[index]`
        """
        item = self._list[sliced]
        del self._list[sliced]
        self.observer(UpdateType.DELETED, item, sliced)

    def __contains__(self, item):
        return item in self._list

    def __iter__(self):
        return iter(self._list)
