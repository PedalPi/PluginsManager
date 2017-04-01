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

import collections

from pluginsmanager.model.updates_observer import UpdatesObserver
from pluginsmanager.model.update_type import UpdateType

from pluginsmanager.util.observable_list import ObservableList

from unittest.mock import MagicMock


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

    def register(self, observer):
        """
        Register an observer for it be notified when occurs changes.

        For more details, see :class:`UpdatesObserver` and :class:`ModHost`.

        :param UpdatesObserver observer: Observer that will be notified then occurs changes
        """
        self.observer_manager.append(observer)
        observer.manager = self

    def append(self, bank):
        """
        Append the bank in banks manager. It will be monitored, changes in this
        will be notified for the notifiers.

        :param Bank bank: Bank that will be added in this
        """
        self.banks.append(bank)

    def _banks_observer(self, update_type, bank, index):
        if update_type == UpdateType.CREATED \
        or update_type == UpdateType.UPDATED:
            bank.manager = self
            bank.observer = self.observer_manager
        elif update_type == UpdateType.DELETED:
            bank.manager = None
            bank.observer_manager = MagicMock()

        self.observer_manager.on_bank_updated(bank, update_type, index=index, origin=self)

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


class ObserverManager(UpdatesObserver):
    def __init__(self):
        super(ObserverManager, self).__init__()
        self.observers = []
        self._observers_scope = collections.deque()

    def enter_scope(self, observer):
        """
        Open a observer scope.

        Informs that changes occurs by the ``observer`` and isn't necessary
        informs the changes for observer

        :param UpdatesObserver observer: Observer that causes changes
        """
        self._observers_scope.append(observer)

    def exit_scope(self):
        """
        Closes the last observer scope added
        """
        self._observers_scope.pop()

    @property
    def scope(self):
        try:
            return self._observers_scope[-1]
        except IndexError:
            return None

    def append(self, observer):
        self.observers.append(observer)

    def on_bank_updated(self, bank, update_type, index, origin, **kwargs):
        for observer in self.observers:
            if observer != self.scope:
                observer.on_bank_updated(bank, update_type, index=index, origin=origin, **kwargs)

    def on_pedalboard_updated(self, pedalboard, update_type, index, origin, **kwargs):
        for observer in self.observers:
            if observer != self.scope:
                observer.on_pedalboard_updated(pedalboard, update_type, index=index, origin=origin, **kwargs)

    def on_effect_updated(self, effect, update_type, index, origin, **kwargs):
        for observer in self.observers:
            if observer != self.scope:
                observer.on_effect_updated(effect, update_type, index=index, origin=origin, **kwargs)

    def on_effect_status_toggled(self, effect, **kwargs):
        for observer in self.observers:
            if observer != self.scope:
                observer.on_effect_status_toggled(effect, **kwargs)

    def on_param_value_changed(self, param, **kwargs):
        for observer in self.observers:
            if observer != self.scope:
                observer.on_param_value_changed(param, **kwargs)

    def on_connection_updated(self, connection, update_type, pedalboard, **kwargs):
        for observer in self.observers:
            if observer != self.scope:
                observer.on_connection_updated(connection, update_type, pedalboard=pedalboard, **kwargs)
