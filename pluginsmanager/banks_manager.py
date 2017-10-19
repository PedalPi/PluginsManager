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

from unittest.mock import MagicMock

from pluginsmanager.observer.update_type import UpdateType
from pluginsmanager.observer.observer_manager import ObserverManager
from pluginsmanager.observer.observable_list import ObservableList


class BanksManager(object):
    """
    BanksManager manager the banks. In these is possible add banks,
    obtains the banks and register observers for will be notified when
    occurs changes (like added new pedalboard, rename bank, set effect
    param value or state)

    For use details, view Readme.rst example documentation.

    :param list[Bank] banks: Banks that will be added in this. Useful
                             for loads banks previously loaded, like
                             banks persisted and recovered.
    """

    def __init__(self, banks=None):
        self.banks = ObservableList()
        self.banks.observer = self._banks_observer

        banks = [] if banks is None else banks
        self.observer_manager = ObserverManager()

        for bank in banks:
            self.append(bank)

    def __iter__(self):
        """
        Iterates banks of the banksmanager::

            >>> banks_manager = BanksManager()
            >>> for index, bank in enumerate(banks_manager):
            ...     print(index, '-', bank)

        :return: Iterator for banks list
        """
        return self.banks.__iter__()

    def register(self, observer):
        """
        Register an observer for it be notified when occurs changes.

        For more details, see :class:`.UpdatesObserver`

        :param UpdatesObserver observer: Observer that will be notified then occurs changes
        """
        self.observer_manager.append(observer)
        observer.manager = self

    def unregister(self, observer):
        """
        Remove the observers of the observers list.
        It will not receive any more notifications when occurs changes.

        :param UpdatesObserver observer: Observer you will not receive any more notifications then
                                         occurs changes.
        """
        self.observer_manager.observers.remove(observer)
        observer.manager = None

    def append(self, bank):
        """
        Append the bank in banks manager. It will be monitored, changes in this
        will be notified for the notifiers.

        :param Bank bank: Bank that will be added in this
        """
        self.banks.append(bank)

    def _banks_observer(self, update_type, bank, index, **kwargs):
        if update_type == UpdateType.CREATED:
            self._init_bank(bank)

        elif update_type == UpdateType.UPDATED:
            self._init_bank(bank)

            old_bank = kwargs['old']
            if old_bank not in self:
                self._clear_bank(old_bank)

        elif update_type == UpdateType.DELETED:
            self._clear_bank(bank)

        self.observer_manager.on_bank_updated(bank, update_type, index=index, origin=self, **kwargs)

    def _init_bank(self, bank):
        bank.manager = self
        bank.observer = self.observer_manager

    def _clear_bank(self, bank):
        bank.manager = None
        bank.observer_manager = MagicMock()

    def enter_scope(self, observer):
        """
        Informs that changes occurs by the ``observer`` and isn't necessary
        informs the changes for observer

        :param UpdatesObserver observer: Observer that causes changes
        """
        self.observer_manager.enter_scope(observer)

    def exit_scope(self):
        """
        Closes the last observer scope added
        """
        self.observer_manager.exit_scope()

    @property
    def observers(self):
        """
        :return: Observers registered in BanksManager instance
        """
        return self.observer_manager.observers
