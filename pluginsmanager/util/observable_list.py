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

from ..model.update_type import UpdateType


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
        """
        See ``__repr__`` :class:`list`
        """
        return repr(self._list)

    def __repr__(self):
        """
        See ``__repr__`` :class:`list`
        """
        return "ObservableList: " + repr(self._list)

    def append(self, item):
        """
        See ``append`` :class:`list` method

        Calls observer ``self.observer(UpdateType.CREATED, item, index)`` where
        **index** is *item position*
        """
        self._list.append(item)
        self.observer(UpdateType.CREATED, item, len(self._list)-1)

    def remove(self, item):
        """
        See ``remove`` :class:`list` method

        Calls observer ``self.observer(UpdateType.DELETED, item, index)`` where
        **index** is *item position*
        """
        index = self.index(item)
        self._list.remove(item)
        self.observer(UpdateType.DELETED, item, index)

    def index(self, x):
        return self._list.index(x)

    def insert(self, index, x):
        """
        See ``insert`` :class:`list` method

        Calls observer ``self.observer(UpdateType.CREATED, item, index)``
        """
        self._list.insert(index, x)
        self.observer(UpdateType.CREATED, x, index)

    def pop(self, index=None):
        """
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
        return len(self._list)

    def __getitem__(self, index):
        return self._list[index]

    def __setitem__(self, index, val):
        """
        See ``__setitem__`` :class:`list` method

        Calls observer ``self.observer(UpdateType.UPDATED, item, index)``
        if ``val != self[index]``
        """
        if val == self[index]:
            return

        old = self._list[index]

        self._list.insert(index+1, val) # Insert and not notify

        exists_other_old_bank_equals = old in self._list[:index] or old in self._list[index+1+1:]
        # Swapped
        if exists_other_old_bank_equals:
            del self._list[index]
        else:
            del self[index] # Notify old has been removed

        self.observer(UpdateType.UPDATED, val, index)

    def __delitem__(self, sliced):
        """
        See ``__delitem__`` :class:`list` method

        Calls observer ``self.observer(UpdateType.DELETED, item, index)``
        where **item** is `self[index]`
        """
        item = self._list[sliced]
        del self._list[sliced]
        self.observer(UpdateType.DELETED, item, sliced)

    def __contains__(self, item):
        """
        See ``__contains__`` :class:`list`
        """
        return item in self._list

    def __iter__(self):
        """
        See ``__iter__`` :class:`list`
        """
        return iter(self._list)
