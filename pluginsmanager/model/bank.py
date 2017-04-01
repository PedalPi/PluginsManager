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

from pluginsmanager.util.observable_list import ObservableList
from pluginsmanager.model.update_type import UpdateType

from unittest.mock import MagicMock
import uuid


class Bank(object):
    """
    Bank is a data structure that contains :class:`Pedalboard`. It's useful
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
        self.name = name
        self.pedalboards = ObservableList()
        self.pedalboards.observer = self._pedalboards_observer

        self.index = -1
        self._uuid = str(uuid.uuid4())

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

    def _pedalboards_observer(self, update_type, pedalboard, index):
        kwargs = {
            'index': index,
            'origin': self
        }

        if update_type == UpdateType.CREATED \
        or update_type == UpdateType.UPDATED:
            pedalboard.bank = self
            pedalboard.observer = self.observer
        elif update_type == UpdateType.DELETED:
            pedalboard.bank = None
            pedalboard.observer = MagicMock()

        self.observer.on_pedalboard_updated(pedalboard, update_type, **kwargs)

    @property
    def json(self):
        """
        Get a json decodable representation of this bank

        :return dict: json representation
        """
        return self.__dict__

    @property
    def __dict__(self):
        return {
            'index': self.index,
            'name': self.name,
            'pedalboards': [pedalboard.json for pedalboard in self.pedalboards]
        }

    def append(self, pedalboard):
        """
        Add a :class:`Pedalboard` in this bank

        This works same as::

        >>> bank.pedalboards.append(pedalboard)

        or::

        >>> bank.pedalboards.insert(len(bank.pedalboards), pedalboard)

        :param Pedalboard pedalboard: Pedalboard that will be added
        """
        self.pedalboards.append(pedalboard)
