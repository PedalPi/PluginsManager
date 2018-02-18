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

import subprocess

from pluginsmanager.observer.host_observer.host_observer import HostObserver
from pluginsmanager.observer.mod_host.host import Host
from pluginsmanager.util.pairs_list import PairsList


class ModHostError(Exception):
    pass


class ModHost(HostObserver):
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

    The changes in current pedalboard (:attr:`~pluginsmanager.observer.mod_host.ModHost.pedalboard`
    attribute of `mod_host`) will also result in mod-host::

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
    :param int port: Socket port on which mod-host should be running. Default is `5555`

    .. _Mod-host: https://github.com/moddevices/mod-host
    .. _LV2: http://lv2plug.in
    .. _Install dependencies: https://github.com/deedos/mod-host/commit/0941d84fc48deb74e27cdcbf23a88db2007d5c6f
    .. _Zoom G3: https://www.zoom.co.jp/products/guitar/g3-guitar-effects-amp-simulator-pedal
    .. _Building mod-host: https://github.com/moddevices/mod-host#building
    .. _Running mod-host: https://github.com/moddevices/mod-host#running
    .. _Demystifying JACK – A Beginners Guide to Getting Started with JACK: http://libremusicproduction.com/articles/demystifying-jack-%E2%80%93-beginners-guide-getting-started-jack
    """

    def __init__(self, address='localhost', port=5555):
        super(ModHost, self).__init__()
        self.address = address
        self.port = port

        self.process = 'mod-host'

        self.host = None
        self._pedalboard = None

        self.pairs_list = PairsList(lambda effect: effect.plugin['uri'])

        self._started_with_this_api = False

    def start(self):
        """
        Invokes the mod-host process.

        mod-host requires JACK to be running.
        mod-host does not startup JACK automatically, so you need to start it before running mod-host.

        .. note::

            This function is experimental. There is no guarantee that the process will actually be initiated.
        """
        if self.address != 'localhost':
            raise ModHostError('The host configured in the constructor isn''t "localhost". '
                               'It is not possible to start a process on another device.')

        try:
            subprocess.call([self.process, '-p', str(self.port)])

        except FileNotFoundError as e:
            exception = ModHostError(
                'mod-host not found. Did you install it? '
                '(https://github.com/moddevices/mod-host#building)'
            )

            raise exception from e

        self._started_with_this_api = True

    def connect(self):
        """
        Connect the object with mod-host with the _address_ parameter informed in
        the constructor method (:meth:`~pluginsmanager.observer.mod_host.ModHost.__init__()`)
        """
        self.host = Host(self.address, self.port)

    def __del__(self):
        """
        Calls :meth:`~pluginsmanager.observer.mod_host.ModHost.close()` method for
        remove the audio plugins loaded and closes connection
        with mod-host.

            >>> mod_host = ModHost()
            >>> del mod_host

        .. note::

            If the mod-host process has been created with :meth:`~pluginsmanager.observer.mod_host.ModHost.start()`
            method, it will be finished.
        """
        self.close()

    def close(self):
        """
        Remove the audio plugins loaded and closes connection with mod-host.

        .. note::

            If the mod-host process has been created with :meth:`~pluginsmanager.observer.mod_host.ModHost.start()`
            method, it will be finished.
        """
        if self.host is None:
            raise ModHostError('There is no established connection with mod-host. '
                               'Did you call the `connect()` method?')

        super(ModHost, self).close()

        if self._started_with_this_api:
            self.host.quit()
        else:
            self.host.close()

    ####################################
    # Observer
    ####################################
    def _set_param_value(self, param):
        self.host.set_param_value(param)

    def _remove_effect(self, effect):
        self.host.remove(effect)

    def _connect(self, connection):
        self.host.connect(connection)

    def _disconnect(self, connection):
        self.host.disconnect(connection)

    def _add_effect(self, effect):
        self.host.add(effect)

    def _set_effect_status(self, effect):
        self.host.set_status(effect)
