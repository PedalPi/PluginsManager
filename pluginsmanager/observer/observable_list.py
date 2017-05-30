# Copyright 2017 SrMouraSilva
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from pluginsmanager.observer.update_type import UpdateType


class ObservableList(object):
    """
    Detects changes in list.

    In append, in remove and in setter, the `observer` is callable with changes
    details

    Based in https://www.pythonsheets.com/notes/python-basic.html#emulating-a-list
    """

    def __init__(self, lista=None):
        self._list = lista if lista is not None else []
        self.observer = lambda *args, **kwargs: ...

    def __str__(self):
        """
        See :meth:`list.__repr__()` method
        """
        return repr(self._list)

    def __repr__(self):
        """
        See :meth:`list.__repr__()` method
        """
        return "ObservableList: " + repr(self._list)

    def append(self, item):
        """
        See :meth:`list.append()` method

        Calls observer ``self.observer(UpdateType.CREATED, item, index)`` where
        **index** is *item position*
        """
        self._list.append(item)
        self.observer(UpdateType.CREATED, item, len(self._list)-1)

    def remove(self, item):
        """
        See :meth:`list.remove()` method

        Calls observer ``self.observer(UpdateType.DELETED, item, index)`` where
        **index** is *item position*
        """
        index = self.index(item)
        self._list.remove(item)
        self.observer(UpdateType.DELETED, item, index)

    def index(self, x):
        """
        See :meth:`list.index()` method
        """
        return self._list.index(x)

    def insert(self, index, x):
        """
        See :meth:`list.insert()` method

        Calls observer ``self.observer(UpdateType.CREATED, item, index)``
        """
        self._list.insert(index, x)
        self.observer(UpdateType.CREATED, x, index)

    def pop(self, index=None):
        """
        See :meth:`list.pop()` method

        Remove the item at the given position in the list, and return it. If no index is specified,
        a.pop() removes and returns the last item in the list.

        :param int index: element index that will be removed

        :return: item removed
        """
        if index is None:
            index = len(self._list) - 1

        item = self[index]
        del self[index]

        return item

    def __len__(self):
        """
        See :meth:`list.__len__()` method
        """
        return len(self._list)

    def __getitem__(self, index):
        """
        See :meth:`list.__getitem__()` method
        """
        return self._list[index]

    def __setitem__(self, index, val):
        """
        See :meth:`list.__setitem__()` method

        Calls observer ``self.observer(UpdateType.UPDATED, item, index)``
        if ``val != self[index]``
        """
        if val == self[index]:
            return

        old = self._list[index]
        self._list[index] = val

        self.observer(UpdateType.UPDATED, val, index, old=old)

    def __delitem__(self, sliced):
        """
        See :meth:`list.__delitem__()` method

        Calls observer ``self.observer(UpdateType.DELETED, item, index)``
        where **item** is `self[index]`
        """
        item = self._list[sliced]
        del self._list[sliced]
        self.observer(UpdateType.DELETED, item, sliced)

    def __contains__(self, item):
        """
        See :meth:`list.__contains__()` method
        """
        return item in self._list

    def __iter__(self):
        """
        See :meth:`list.__iter__()` method
        """
        return iter(self._list)

    def move(self, item, new_position):
        """
        Moves a item list to new position

        Calls observer ``self.observer(UpdateType.DELETED, item, index)``
        and observer ``self.observer(UpdateType.CREATED, item, index)``
        if ``val != self[index]``

        :param item: Item that will be moved to new_position
        :param new_position: Item's new position
        """
        if item == self[new_position]:
            return

        self.remove(item)
        self.insert(new_position, item)
