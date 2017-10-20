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

import sys
from pathlib import Path

from pluginsmanager.model.pedalboard import Pedalboard
from pluginsmanager.model.system.system_effect import SystemEffect


class ModPedalboardConverter(object):
    """
    ModPedalboardConverter is a utility to convert MOD pedalboards structure
    in plugins manager pedalboard.

    `MOD`_, an awesome music enterprise, create the `mod-ui`_, a visual interface
    that enable create pedalboards in a simple way.

    .. _MOD: http://moddevices.com/
    .. _mod-ui: https://github.com/moddevices/mod-ui
    """

    def __init__(self, mod_ui_path, builder):
        """
        :param Path mod_ui_path: path that mod_ui has in the computer.
        :param Lv2EffectBuilder builder: Builder for generate the lv2 effects
        """
        self._load_mod_ui_libraries(mod_ui_path)
        self.builder = builder

    def _load_mod_ui_libraries(self, path):
        """
        :param Path path:
        """
        path = path / Path('mod')
        sys.path.append(str(path))

    def get_pedalboard_info(self, path):
        """
        :param Path path: Path that the pedalboard has been persisted.
                          Generally is in format `path/to/pedalboard/name.pedalboard`
        :return dict: pedalboard persisted configurations
        """
        from utils import get_pedalboard_info

        return get_pedalboard_info(str(path))

    def convert(self, pedalboard_path, system_effect):
        """
        :param Path pedalboard_path: Path that the pedalboard has been persisted.
                                     Generally is in format `path/to/pedalboard/name.pedalboard`
        :param SystemEffect system_effect: Effect that contains the audio interface outputs and inputs
        :return Pedalboard: Pedalboard loaded
        """
        info = self.get_pedalboard_info(pedalboard_path)

        pedalboard = Pedalboard(info['title'])

        effects_instance = {}

        for effect_data in info['plugins']:
            effect = self._generate_effect(effect_data)
            pedalboard.append(effect)
            effects_instance[effect_data['instance']] = effect

        for connection_data in info['connections']:
            output_port = self._get_port(connection_data['source'], effects_instance, system_effect)
            input_port = self._get_port(connection_data['target'], effects_instance, system_effect)

            pedalboard.connect(output_port, input_port)

        return pedalboard

    def _generate_effect(self, effect_data):
        effect = self.builder.build(effect_data['uri'])
        effect.active = not effect_data['bypassed']

        for param_data in effect_data['ports']:
            effect.params[param_data['symbol']].value = param_data['value']

        return effect

    def _get_port(self, name, effects_instance, system_effect):
        effect, port = None, None

        if name.startswith('capture_') or name.startswith('playback_'):
            effect = system_effect
            port = name
        else:
            instance, port = name.split('/')
            effect = effects_instance[instance]

        possible_ports = (effect.outputs, effect.inputs, effect.midi_outputs, effect.midi_inputs)
        filtered = filter(lambda ports: port in ports, possible_ports)

        ports = list(filtered)[0]
        return ports[port]

