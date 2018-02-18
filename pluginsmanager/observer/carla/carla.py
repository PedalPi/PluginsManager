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

#FIXME
#from carla_backend import CarlaHostDLL, ENGINE_OPTION_PATH_BINARIES, BINARY_NATIVE, PLUGIN_LV2


class CarlaError(Exception):
    pass


class Carla(HostObserver):
    """
    **Python port for carla**
        `Carla`_ is a fully-featured audio plugin host, with support for many audio drivers and plugin formats.
        It's open source and licensed under the GNU General Public License, version 2 or later.

    This class offers the Carla control in a python API::

        # Create a carla, connect and register it in banks_manager
        host = Carla('localhost')
        host.connect()
        banks_manager.register(host)

        # Set the carla.pedalboard for a pedalboard that the bank
        # has added in banks_manager
        host.pedalboard = my_awesome_pedalboard

    The changes in current pedalboard (:attr:`~pluginsmanager.observer.carla.Carla.pedalboard`
    attribute of `carla`) will also result in carla host::

        driver = my_awesome_pedalboard.effects[0]
        driver.active = False

    .. note::

        For use, is necessary that the carla is running, for use, access

         * Install dependencies
         * Building Carla
         * Running Carla

        For more JACK information, access `Demystifying JACK – A Beginners Guide to Getting Started with JACK`_

    **Example:**

        In this example, is starting a `Zoom G3`_ series audio interface. Others interfaces
        maybe needs others configurations.

    .. code-block:: bash

        # Starting jackdump process via console
        jackd -R -P70 -t2000 -dalsa -dhw:Series -p256 -n3 -r44100 -s &
        # Starting carla host
        # FIXME

    :param Path path: Path that carla are persisted.

    .. _Carla: https://github.com/falkTX/Carla
    .. _LV2: http://lv2plug.in
    .. _Zoom G3: https://www.zoom.co.jp/products/guitar/g3-guitar-effects-amp-simulator-pedal
    .. _Demystifying JACK – A Beginners Guide to Getting Started with JACK: http://libremusicproduction.com/articles/demystifying-jack-%E2%80%93-beginners-guide-getting-started-jack
    """

    def __init__(self, path):
        super(Carla, self).__init__()

        self.index = 0

        self.host = CarlaHostDLL(path / "libcarla_standalone2.so", False)
        self.host.set_engine_option(ENGINE_OPTION_PATH_BINARIES, 0, path)

    def _connect(self, connection):
        # TODO
        # https://github.com/moddevices/mod-ui/blob/master/mod/host_carla.py#L185-L198
        split_from = port_from.split("/")
        if len(split_from) != 3:
            return
        if split_from[1] == "system":
            groupIdA = self._client_id_system
            portIdA  = int(split_from[2].rsplit("_",1)[-1])
            instance_from, port_from = port_from.rsplit("/", 1)
        else:
            groupIdB = self._getPluginId(split_from[:1].join("/"))
            portIdB  = int(split_from[2].rsplit("_",1)[-1])
            instance_from, port_from = port_from.rsplit("/", 1)

        self.host.patchbay_connect(groupIdA, portIdA, groupIdB, portIdB)

    def _disconnect(self, connection):
        pass

    def _add_effect(self, effect):
        if not self.host.add_plugin(
                BINARY_NATIVE,
                PLUGIN_LV2,
                None,#"/usr/lib/lv2/gx_echo.lv2/gx_echo.so",  # Fixme
                "effect_{}".format(effect.index),
                effect.plugin.json['uri'],
                0,
                None,
                0):
            CarlaError("Failed to load plugin, possible reasons:\n%s" % self.host.get_last_error())

    def _remove_effect(self, effect):
        self.host.add_plugin(effect.index)

    def _set_effect_status(self, effect):
        self.host.set_active(effect.index, effect.active)

    def _set_param_value(self, param):
        effect_index = param.effect.index
        param_index = param.data['index']
        self.host.set_parameter_value(effect_index, param_index, param.value)
