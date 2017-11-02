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

from abc import ABCMeta
from pluginsmanager.observer.observable_list import ObservableList


class AlreadyAddedError(Exception):
    pass


class NotAddableError(Exception):
    pass


class RestrictionList(metaclass=ABCMeta):
    """
    List with validation when add a element
    """

    def __init__(self):
        self._items = set()
        self.real_list = ObservableList()

    @property
    def observer(self):
        return self.real_list.observer

    @observer.setter
    def observer(self, observer):
        self.real_list.observer = observer

    def check_insertion(self, item):
        pass

    def __str__(self):
        """
        See :meth:`~pluginsmanager.observer.observable_list.ObservableList.__repr__()` method
        """
        return repr(self.real_list)

    def __repr__(self):
        """
        See :meth:`~pluginsmanager.observer.observable_list.ObservableList.__repr__()` method
        """
        return repr(self.real_list)

    def append(self, item):
        """
        See :meth:`~pluginsmanager.observer.observable_list.ObservableList.append()` method
        """
        self.check_insertion(item)

        self.real_list.append(item)
        self._items |= {item}

    def remove(self, item):
        """
        See :meth:`~pluginsmanager.observer.observable_list.ObservableList.remove()` method
        """
        self.real_list.remove(item)
        self._items.remove(item)

    def remove_silently(self, item):
        """
        Remove item and not notify
        """
        self.real_list.real_list.remove(item)
        self._items.remove(item)

    def index(self, x):
        """
        See :meth:`~pluginsmanager.observer.observable_list.ObservableList.index()` method
        """
        return self.real_list.index(x)

    def insert(self, index, x):
        """
        See :meth:`~pluginsmanager.observer.observable_list.ObservableList.insert()` method
        """
        self.check_insertion(x)

        self.real_list.insert(index, x)
        self._items |= {x}

    def pop(self, index=None):
        """
        See :meth:`~pluginsmanager.observer.observable_list.ObservableList.pop()` method
        """
        if index is None:
            index = len(self.real_list) - 1

        effect = self[index]
        returned = self.real_list.pop(index)

        self._items.remove(effect)
        return returned

    def __len__(self):
        """
        See :meth:`~pluginsmanager.observer.observable_list.ObservableList.__len__()` method
        """
        return len(self.real_list)

    def __getitem__(self, index):
        """
        See :meth:`~pluginsmanager.observer.observable_list.ObservableList.__getitem__()` method
        """
        return self.real_list.__getitem__(index)

    def __setitem__(self, index, val):
        """
        See :meth:`~pluginsmanager.observer.observable_list.ObservableList.__setitem__()` method

        Swap doesn't works::

            >>> builder = Lv2EffectBuilder()
            >>> effects = EffectsList()
            >>> effects.append(builder.build('http://calf.sourceforge.net/plugins/Reverb'))
            >>> effects.append(builder.build('http://guitarix.sourceforge.net/plugins/gx_fuzzfacefm_#_fuzzfacefm_'))
            >>> effects[0], effects[1] = effects[1], effects[0]
            pluginsmanager.model.effects_list.AlreadyAddedError: The effect 'GxFuzzFaceFullerMod' already added

        """
        if val == self[index]:
            return

        self.check_insertion(val)

        old = self.real_list[index]
        self._items.remove(old)
        self.real_list.__setitem__(index, val)
        self._items |= {val}

    def __delitem__(self, sliced):
        """
        See :meth:`~pluginsmanager.observer.observable_list.ObservableList.__delitem__()` method
        """
        item = self.real_list[sliced]
        self.real_list.__delitem__(sliced)
        self._items.remove(item)

    def __contains__(self, item):
        """
        See :meth:`~pluginsmanager.observer.observable_list.ObservableList.__contains__()` method
        """
        return item in self._items

    def __iter__(self):
        """
        See :meth:`~pluginsmanager.observer.observable_list.ObservableList.__iter__()` method
        """
        return iter(self.real_list)

    def move(self, item, new_position):
        """
        See :meth:`~pluginsmanager.observer.observable_list.ObservableList.move()` method
        """
        self.real_list.move(item, new_position)
