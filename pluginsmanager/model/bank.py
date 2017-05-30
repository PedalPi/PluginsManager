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

from pluginsmanager.observer.observable_list import ObservableList
from pluginsmanager.observer.update_type import UpdateType

from unittest.mock import MagicMock
from pluginsmanager.observer.autosaver.indexable import Indexable


class Bank(Indexable):
    """
    Bank is a data structure that contains :class:`.Pedalboard`. It's useful
    for group common pedalboards, like "Pedalboards will be used in
    the Sunday show"

    A fast bank overview::

    >>> bank = Bank('RHCP')
    >>> californication = Pedalboard('Californication')

    >>> # Add pedalboard in bank - mode A
    >>> bank.append(californication)
    >>> californication.bank == bank
    True

    >>> bank.pedalboards[0] == californication
    True

    >>> # Add pedalboard in bank - mode B
    >>> bank.pedalboards.append(Pedalboard('Dark Necessities'))
    >>> bank.pedalboards[1].bank == bank
    True

    >>> # If you needs change pedalboards order (swap), use pythonic mode
    >>> bank.pedalboards[1], bank.pedalboards[0] = bank.pedalboards[0], bank.pedalboards[1]
    >>> bank.pedalboards[1] == californication
    True

    >>> # Set pedalboard
    >>> bank.pedalboards[0] = Pedalboard("Can't Stop")
    >>> bank.pedalboards[0].bank == bank
    True

    >>> del bank.pedalboards[0]
    >>> bank.pedalboards[0] == californication # Pedalboard Can't stop rermoved, first is now the californication
    True

    You can also toggle pedalboards into different banks::

    >>> bank1.pedalboards[0], bank2.pedalboards[2] = bank2.pedalboards[0], bank1.pedalboards[2]

    :param string name: Bank name
    """
    def __init__(self, name):
        super(Bank, self).__init__()

        self.name = name
        self.pedalboards = ObservableList()
        self.pedalboards.observer = self._pedalboards_observer

        self.manager = None

        self._observer = MagicMock()

    @property
    def observer(self):
        return self._observer

    @observer.setter
    def observer(self, observer):
        self._observer = observer
        for pedalboard in self.pedalboards:
            pedalboard.observer = observer

    def _pedalboards_observer(self, update_type, pedalboard, index, **kwargs):
        kwargs['index'] = index
        kwargs['origin'] = self

        if update_type == UpdateType.CREATED:
            self._init_pedalboard(pedalboard)

        elif update_type == UpdateType.UPDATED:
            self._init_pedalboard(pedalboard)

            old_pedalboard = kwargs['old']
            if old_pedalboard not in self.pedalboards:
                self._clear_pedalboard(old_pedalboard)

        elif update_type == UpdateType.DELETED:
            self._clear_pedalboard(pedalboard)

        self.observer.on_pedalboard_updated(pedalboard, update_type, **kwargs)

    def _init_pedalboard(self, pedalboard):
        pedalboard.bank = self
        pedalboard.observer = self.observer

    def _clear_pedalboard(self, pedalboard):
        pedalboard.bank = None
        pedalboard.observer = MagicMock()

    @property
    def json(self):
        """
        Get a json decodable representation of this bank

        :return dict: json representation
        """
        return self.__dict__

    @property
    def __dict__(self):
        try:
            index = self.index
        except IndexError:
            index = -1

        return {
            'index': index,
            'name': self.name,
            'pedalboards': [pedalboard.json for pedalboard in self.pedalboards]
        }

    def append(self, pedalboard):
        """
        Add a :class:`.Pedalboard` in this bank

        This works same as::

        >>> bank.pedalboards.append(pedalboard)

        or::

        >>> bank.pedalboards.insert(len(bank.pedalboards), pedalboard)

        :param Pedalboard pedalboard: Pedalboard that will be added
        """
        self.pedalboards.append(pedalboard)

    @property
    def index(self):
        """
        Returns the first occurrence of the bank in your :class:`.PluginsManager`
        """
        if self.manager is None:
            raise IndexError('Bank not contains a manager')

        return self.manager.banks.index(self)

    @property
    def simple_identifier(self):
        return self.name
