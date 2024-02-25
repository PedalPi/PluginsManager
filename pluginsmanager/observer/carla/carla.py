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
from pathlib import Path

from pluginsmanager.observer.carla.carla_host import CarlaHost, CarlaError
from pluginsmanager.observer.host_observer.host_observer import HostObserver


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

    def __init__(self, path: Path):
        super(Carla, self).__init__()

        self.host = CarlaHost(path, 'Pedal Pi')
        self.index = 0  # Needs to start with zero to works correctly (carlaHostDLL.carla_get_current_plugin_count())

    def connect(self):
        raise CarlaError("Please, call start instead connect")

    def start(self):
        self.host.start()

    def close(self):
        self.host.stop()

    def _connect(self, connection):
        self.host.connect(connection.output, connection.input)

    def _disconnect(self, connection):
        self.host.disconnect(connection.output, connection.input)

    def _add_effect(self, effect):
        plugin_bin = f"/usr/lib/lv2/{effect.plugin.data['bundle_name']}/{effect.plugin.data['binary']}"
        plugin_uri = effect.plugin.data['uri']
        effect_name = f"effect_{self.index}"

        self.index += 1

        self.host.add_effect(plugin_bin, plugin_uri, effect_name, effect)

    def _remove_effect(self, effect):
        self.host.remove_effect(effect)

    def _set_effect_status(self, effect):
        self.host.set_active(effect, effect.active)

    def _set_param_value(self, param):
        self.host.set_parameter_value(param)
