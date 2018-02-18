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

from pluginsmanager.observer.update_type import UpdateType
from pluginsmanager.observer.updates_observer import UpdatesObserver
from pluginsmanager.util.pairs_list import PairsList


class HostError(Exception):
    pass


class HostObserver(UpdatesObserver, metaclass=ABCMeta):
    """
    :class:`.HostObserver` contains the basis for Host implementations, like
    :class:`.ModHost` or :class:`.Carla`.

    It is an :class:`UpdatesObserver`. With it, can be apply the current
    pedalboard changes transparently.

    HostObserver contains an algorithm for improve the change of the
    current pedalboard. Also, HostObserver process the updates and define
    abstract methods that hosts needs to implements, usually only with the
    important part.
    """
    
    def __init__(self):
        super(HostObserver, self).__init__()
        self._pedalboard = None

        self.pairs_list = PairsList(lambda effect: effect.plugin['uri'])

    def start(self):
        """
        Invokes the process.
        """
        pass

    def connect(self):
        """
        Connect with the host
        """
        pass

    @property
    def pedalboard(self):
        """
        Currently managed pedalboard (current pedalboard)

        :getter: Current pedalboard - Pedalboard loaded by mod-host
        :setter: Set the pedalboard that will be loaded by mod-host
        :type: Pedalboard
        """
        return self._pedalboard

    @pedalboard.setter
    def pedalboard(self, pedalboard):
        self.on_current_pedalboard_changed(pedalboard)

    def __del__(self):
        """
        Calls :meth:`~pluginsmanager.observer.host_observer.host_observer.HostObserver.close()` method for
        remove the audio plugins loaded and closes connection
        with the host.
        """
        self.close()

    def close(self):
        """
        Remove the audio plugins loaded and closes connection with the host.
        """
        self.pedalboard = None

    ####################################
    # Observer
    ####################################
    def on_current_pedalboard_changed(self, pedalboard, **kwargs):
        if self.pedalboard is not None and pedalboard is not None:
            self._replace_pedalboard(self.pedalboard, pedalboard)
        else:
            self._change_pedalboard(pedalboard)

    def on_bank_updated(self, bank, update_type, **kwargs):
        if (self.pedalboard is not None
        and bank != self.pedalboard.bank):
            return
        pass

    def on_pedalboard_updated(self, pedalboard, update_type, **kwargs):
        if pedalboard != self.pedalboard:
            return

        self.on_current_pedalboard_changed(pedalboard)

    def on_effect_updated(self, effect, update_type, index, origin, **kwargs):
        if origin != self.pedalboard:
            return

        if update_type == UpdateType.CREATED:
            self._add_effect(effect)
            self._load_params_of(effect)
            self.on_effect_status_toggled(effect)

        if update_type == UpdateType.DELETED:
            self._remove_effect(effect)

    def _load_params_of(self, effect):
        """
        Called only when a effect has created
        Param changes calls :meth:`~pluginsmanager.observer.host_observer.host_observer.HostObserver.on_param_value_changed()`
        """
        for param in effect.params:
            if param.value != param.default:
                self._set_param_value(param)

    def on_effect_status_toggled(self, effect, **kwargs):
        if effect.pedalboard != self.pedalboard:
            return

        self._set_effect_status(effect)

    def on_param_value_changed(self, param, **kwargs):
        if param.effect.pedalboard != self.pedalboard:
            return

        self._set_param_value(param)

    def on_connection_updated(self, connection, update_type, pedalboard, **kwargs):
        if pedalboard != self.pedalboard:
            return

        if update_type == UpdateType.CREATED:
            self._connect(connection)
        elif update_type == UpdateType.DELETED:
            self._disconnect(connection)

    ####################################
    # Private methods
    ####################################
    def _replace_pedalboard(self, current, pedalboard):
        # Replace effects with equal plugins
        result = self.pairs_list.calculate(current.effects, pedalboard.effects)

        for current_effect, new_effect in result.pairs:
            new_effect.instance = current_effect.instance

            for parameter_old_effect, parameter_new_effect in zip(current_effect.params, new_effect.params):
                if parameter_new_effect.value != parameter_old_effect.value:
                    self._set_param_value(parameter_new_effect)

        # Remove not equal plugins
        current_will_remove = result.elements_not_added_a

        self._remove_connections_of(current)
        self._remove_effects(current_will_remove)

        self._pedalboard = pedalboard

        # Remove not equal plugins
        # Changes are only updated if self._pedalboard = pedalboard
        pedalboard_will_add = result.elements_not_added_b

        self._add_effects(pedalboard_will_add)
        self._add_connections_of(pedalboard)

    def _change_pedalboard(self, pedalboard):
        if self.pedalboard is not None:
            self._remove_pedalboard(self.pedalboard)

        self._pedalboard = pedalboard

        # Changes are only updated if self._pedalboard = pedalboard
        if pedalboard is not None:
            self._add_effects(pedalboard.effects)
            self._add_connections_of(pedalboard)

    def _remove_pedalboard(self, pedalboard):
        self._remove_effects(pedalboard.effects)
        self._remove_connections_of(pedalboard)

    def _remove_connections_of(self, pedalboard):
        for connection in pedalboard.connections:
            self.on_connection_updated(connection, UpdateType.DELETED, pedalboard=pedalboard)

    def _remove_effects(self, effects):
        for effect in effects:
            self.on_effect_updated(effect, UpdateType.DELETED, index=None, origin=effect.pedalboard)

    def _add_connections_of(self, pedalboard):
        for connection in pedalboard.connections:
            self.on_connection_updated(connection, UpdateType.CREATED, pedalboard=pedalboard)

    def _add_effects(self, effects):
        for effect in effects:
            self.on_effect_updated(effect, UpdateType.CREATED, index=None, origin=effect.pedalboard)

    ####################################
    # Implementation
    ####################################
    @abstractmethod
    def _add_effect(self, effect):
        pass

    @abstractmethod
    def _remove_effect(self, effect):
        pass

    @abstractmethod
    def _connect(self, connection):
        pass

    @abstractmethod
    def _disconnect(self, connection):
        pass

    @abstractmethod
    def _set_param_value(self, param):
        pass

    @abstractmethod
    def _set_effect_status(self, effect):
        pass
