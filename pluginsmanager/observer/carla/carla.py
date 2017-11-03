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

from pluginsmanager.observer.host_observer.host_observer import HostObserver

from carla_backend import CarlaHostDLL, ENGINE_OPTION_PATH_BINARIES, BINARY_NATIVE, PLUGIN_LV2


class CarlaError(Exception):
    pass


class Carla(HostObserver):
    """
    **Python port for carla**
        `Carla`_ is a fully-featured audio plugin host, with support for many audio drivers and plugin formats.
        It's open source and licensed under the GNU General Public License, version 2 or later.

    This class offers the mod-host control in a python API::

        # Create a mod-host, connect and register it in banks_manager
        mod_host = ModHost('localhost')
        mod_host.connect()
        banks_manager.register(mod_host)

        # Set the mod_host pedalboard for a pedalboard that the bank
        # has added in banks_manager
        mod_host.pedalboard = my_awesome_pedalboard

    The changes in current pedalboard (:attr:`~pluginsmanager.observer.carla.Carla.pedalboard`
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

    .. _Carla: https://github.com/falkTX/Carla
    .. _LV2: http://lv2plug.in
    .. _Install dependencies: https://github.com/deedos/mod-host/commit/0941d84fc48deb74e27cdcbf23a88db2007d5c6f
    .. _Zoom G3: https://www.zoom.co.jp/products/guitar/g3-guitar-effects-amp-simulator-pedal
    .. _Building mod-host: https://github.com/moddevices/mod-host#building
    .. _Running mod-host: https://github.com/moddevices/mod-host#running
    .. _Demystifying JACK – A Beginners Guide to Getting Started with JACK: http://libremusicproduction.com/articles/demystifying-jack-%E2%80%93-beginners-guide-getting-started-jack
    """

    def __init__(self, path):
        super(Carla, self).__init__()

        self.index = 0

        self.host = CarlaHostDLL(path / "libcarla_standalone2.so", False)
        self.host.set_engine_option(ENGINE_OPTION_PATH_BINARIES, 0, path)

    def _connect(self, connection):
        pass

    def _disconnect(self, connection):
        pass

    def _add_effect(self, effect):
        if not self.host.add_plugin(
                BINARY_NATIVE,
                PLUGIN_LV2,
                "/usr/lib/lv2/gx_echo.lv2/gx_echo.so",  # Fixme
                "effect_{}".format(effect.index),
                effect.plugin.json['uri'],
                0,
                None,
                0):
            print("Failed to load plugin, possible reasons:\n%s" % self.host.get_last_error())

    def _remove_effect(self, effect):
        self.host.add_plugin(effect.index)

    def _set_effect_status(self, effect):
        self.host.set_active(effect.index, effect.active)

    def _set_param_value(self, param):
        effect_index = param.effect.index
        param_index = param._param['index']
        self.host.set_parameter_value(effect_index, param_index, param.value)
