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

from abc import ABCMeta, abstractmethod


class UpdatesObserver(metaclass=ABCMeta):
    """
    The :class:`.UpdatesObserver` is an abstract class definition for
    treatment of changes in some class model. Your methods are called
    when occurs any change in :class:`.Bank`, :class:`.Pedalboard`,
    :class:`.Effect`, etc.

    To do this, it is necessary that the :class:`.UpdatesObserver` objects
    be registered in some manager, so that it reports the changes. An
    example of a manager is :class:`.BanksManager`.
    """

    def __init__(self):
        self.manager = None

    def __enter__(self):
        if self.manager is not None:
            self.manager.enter_scope(self)

    def __exit__(self, type, value, traceback):
        if self.manager is not None:
            self.manager.exit_scope()

    @abstractmethod
    def on_bank_updated(self, bank, update_type, index, origin, **kwargs):
        """
        Called when changes occurs in any :class:`.Bank`

        :param Bank bank: Bank changed.
        :param UpdateType update_type: Change type
        :param int index: Bank index (or old index if update_type == UpdateType.DELETED)
        :param BanksManager origin: BanksManager that the bank is (or has) contained
        :param Bank: Contains the old bank occurs a `UpdateType.UPDATED`
        """
        pass

    @abstractmethod
    def on_pedalboard_updated(self, pedalboard, update_type, index, origin, **kwargs):
        """
        Called when changes occurs in any :class:`.Pedalboard`

        :param Pedalboard pedalboard: Pedalboard changed
        :param UpdateType update_type: Change type
        :param int index: Pedalboard index (or old index if update_type == UpdateType.DELETED)
        :param Bank origin: Bank that the pedalboard is (or has) contained
        :param Pedalboard old: Contains the old pedalboard when occurs a `UpdateType.UPDATED`
        """
        pass

    @abstractmethod
    def on_effect_updated(self, effect, update_type, index, origin, **kwargs):
        """
        Called when changes occurs in any :class:`.Effect`

        :param Effect effect: Effect changed
        :param UpdateType update_type: Change type
        :param int index: Effect index (or old index if update_type == UpdateType.DELETED)
        :param Pedalboard origin: Pedalboard that the effect is (or has) contained
        """
        pass

    @abstractmethod
    def on_effect_status_toggled(self, effect, **kwargs):
        """
        Called when any :class:`.Effect` status is toggled

        :param Effect effect: Effect when status has been toggled
        """
        pass

    @abstractmethod
    def on_param_value_changed(self, param, **kwargs):
        """
        Called when a param value change

        :param Param param: Param with value changed
        """
        pass

    @abstractmethod
    def on_connection_updated(self, connection, update_type, pedalboard, **kwargs):
        """
        Called when changes occurs in any :class:`pluginsmanager.model.connection.Connection` of Pedalboard
        (adding, updating or removing connections)

        :param pluginsmanager.model.connection.Connection connection: Connection changed
        :param UpdateType update_type: Change type
        :param Pedalboard pedalboard: Pedalboard that the connection is (or has) contained
        """
        pass
