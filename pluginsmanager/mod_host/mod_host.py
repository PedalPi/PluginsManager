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

from pluginsmanager.model.updates_observer import UpdatesObserver
from pluginsmanager.model.update_type import UpdateType

from pluginsmanager.model.connection import Connection

from pluginsmanager.mod_host.host import Host


class ModHost(UpdatesObserver):
    """
    **Python port for mod-host**
        `Mod-host`_ is a `LV2`_ host for Jack controllable via socket or command line.

    This class offers the mod-host control in a python API::

        # Create a mod-host, connect and register it in banks_manager
        mod_host = ModHost('localhost')
        mod_host.connect()
        banks_manager.register(mod_host)

        # Set the mod_host pedalboard for a pedalboard that the bank
        # has added in banks_manager
        mod_host.pedalboard = my_awesome_pedalboard

    The changes in current pedalboard (``mod_host.pedalboard``) will also result in mod-host::

        driver = my_awesome_pedalboard.effects[0]
        driver.active = False

    .. note::

        For use, is necessary that the mod-host is running, for use, access

         * `Install dependencies`_
         * `Building mod-host`_
         * `Running mod-host`_

        For more JACK information, access `Demystifying JACK – A Beginners Guide to Getting Started with JACK`_

    **Example:**

        In this example, is starting a `Zoom G3`_ series audio interface. Others interfaces
        maybe needs others configurations.

    .. code-block:: bash

        # Starting jackdump process via console
        jackd -R -P70 -t2000 -dalsa -dhw:Series -p256 -n3 -r44100 -s &
        # Starting mod-host
        mod-host &

    :param string address: Computer mod-host process address (IP). If the
     process is running on the same computer that is running the python code
     uses `localhost`.

    .. _Mod-host: https://github.com/moddevices/mod-host
    .. _LV2: http://lv2plug.in
    .. _Install dependencies: https://github.com/deedos/mod-host/commit/0941d84fc48deb74e27cdcbf23a88db2007d5c6f
    .. _Zoom G3: https://www.zoom.co.jp/products/guitar/g3-guitar-effects-amp-simulator-pedal
    .. _Building mod-host: https://github.com/moddevices/mod-host#building
    .. _Running mod-host: https://github.com/moddevices/mod-host#running
    .. _Demystifying JACK – A Beginners Guide to Getting Started with JACK: http://libremusicproduction.com/articles/demystifying-jack-%E2%80%93-beginners-guide-getting-started-jack
    """

    def __init__(self, address='localhost'):
        super(ModHost, self).__init__()
        self.address = address

        self.host = None
        self._pedalboard = None

    def connect(self):
        """
        Connect the object with mod-host with the _address_ parameter informed in
        the initialization (``__init__(address)``)
        """
        self.host = Host(self.address)

    def auto_connect(self):
        if self.pedalboard is None or len(self.pedalboard.effects) == 0:
            return

        first = self.pedalboard.effects[0]
        last = self.pedalboard.effects[-1]

        self.host.connect_input_in(first.inputs[0])

        before = first
        for effect in self.pedalboard.effects[1:]:
            self.host.connect(Connection(before.outputs[0], effect.inputs[0]))
            before = effect

        self.host.connect_on_output(last.outputs[0], 1)
        self.host.connect_on_output(last.outputs[0], 2)

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
        if self.pedalboard:
            self._remove_pedalboard(self.pedalboard)

    ####################################
    # Observer
    ####################################
    def on_current_pedalboard_changed(self, pedalboard):
        if self.pedalboard is not None:
            self._remove_pedalboard(self.pedalboard)

        self._pedalboard = pedalboard

        # Changes are only updated if self._pedalboard = pedalboard
        if pedalboard is not None:
            for index, effect in enumerate(pedalboard.effects):
                self.on_effect_updated(effect, UpdateType.CREATED, index=index, origin=pedalboard)

            for connection in pedalboard.connections:
                self.on_connection_updated(connection, UpdateType.CREATED, pedalboard=pedalboard)

    def _remove_pedalboard(self, pedalboard):
        for index, effect in enumerate(pedalboard.effects):
            self.on_effect_updated(effect, UpdateType.DELETED, index=index, origin=pedalboard)

    def on_bank_updated(self, bank, update_type, **kwargs):
        if self.pedalboard is not None \
        and bank != self.pedalboard.bank:
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
            self.host.add(effect)
            self._load_params_of(effect)
            self.on_effect_status_toggled(effect)

        if update_type == UpdateType.DELETED:
            self.host.remove(effect)

    def _load_params_of(self, effect):
        for param in effect.params:
            if param.value != param.default:
                self._set_param_value(param)

    def on_effect_status_toggled(self, effect):
        if effect.pedalboard != self.pedalboard:
            return

        self.host.set_status(effect)

    def on_param_value_changed(self, param):
        if param.effect.pedalboard != self.pedalboard:
            return

        self._set_param_value(param)

    def on_connection_updated(self, connection, update_type, pedalboard, **kwargs):
        if pedalboard != self.pedalboard:
            return

        if update_type == UpdateType.CREATED:
            self.host.connect(connection)
        elif update_type == UpdateType.DELETED:
            self.host.disconnect(connection)

    def _set_param_value(self, param):
        self.host.set_param_value(param)
