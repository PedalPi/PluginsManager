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


class PortNotFoundError(Exception):
    pass


class ModPedalboardConverter(object):
    """
    ModPedalboardConverter is a utility to convert MOD [#]_ pedalboards structure
    in plugins manager pedalboard.

    For use, is necessary that the computer system contains the mod_ui with your codes compiled [#]_
    and the pedalboard::

    >>> path = Path('/home/user/git/mod/mod_ui/')
    >>> builder = Lv2EffectBuilder()
    >>> converter = ModPedalboardConverter(path, builder)
    >>> pedalboard_path = Path('/home/user/.pedalboards/pedalboard_name.pedalboard')
    >>> system_effect = SystemEffect('system', ['capture_1', 'capture_2'], ['playback_1', 'playback_2'])
    >>> pedalboard = converter.convert(pedalboard_path, system_effect)

    ModPedalboardConverter can try discover the `system_pedalboard` by the pedalboard::

    >>> path = Path('/home/user/git/mod/mod_ui/')
    >>> builder = Lv2EffectBuilder()
    >>> converter = ModPedalboardConverter(path, builder)
    >>> pedalboard_path = Path('/home/user/.pedalboards/pedalboard_name.pedalboard')
    >>> pedalboard = converter.convert(pedalboard_path)

    If you needs only obtain the system effect::

    >>> path = Path('/home/user/git/mod/mod_ui/')
    >>> builder = Lv2EffectBuilder()
    >>> converter = ModPedalboardConverter(path, builder)
    >>> pedalboard_path = Path('/home/user/.pedalboards/pedalboard_name.pedalboard')
    >>> pedalboard_info = converter.get_pedalboard_info(pedalboard_path)
    >>> system_effect = converter.discover_system_effect(pedalboard_info)

    .. [#] `MOD`_, an awesome music enterprise, create the `mod-ui`_, a visual interface
           that enable create pedalboards in a simple way.
    .. [#] See the docs: https://github.com/moddevices/mod-ui#install

    .. _MOD: http://moddevices.com/
    .. _mod-ui: https://github.com/moddevices/mod-ui

    :param Path mod_ui_path: path that mod_ui has in the computer.
    :param Lv2EffectBuilder builder: Builder for generate the lv2 effects
    :param bool ignore_errors: Ignore pedalboard problems like connections with undefined ports
    """

    def __init__(self, mod_ui_path, builder, ignore_errors=False):
        self._load_mod_ui_libraries(mod_ui_path)
        self.builder = builder
        self.ignore_errors = ignore_errors

    def _load_mod_ui_libraries(self, path):
        """
        :param Path path:
        """
        path = path / Path('mod')
        sys.path.append(str(path))

    def get_pedalboard_info(self, path):
        """
        :param Path path: Path that the pedalboard has been persisted.
                          Generally is in format ``path/to/pedalboard/name.pedalboard``
        :return dict: pedalboard persisted configurations
        """
        from utils import get_pedalboard_info

        return get_pedalboard_info(str(path))

    def convert(self, pedalboard_path, system_effect=None):
        """
        :param Path pedalboard_path: Path that the pedalboard has been persisted.
                                     Generally is in format `path/to/pedalboard/name.pedalboard`
        :param SystemEffect system_effect: Effect that contains the audio interface outputs and inputs
                                           or None for **auto discover**
        :return Pedalboard: Pedalboard loaded
        """
        info = self.get_pedalboard_info(pedalboard_path)

        if system_effect is None:
            system_effect = self.discover_system_effect(info)

        pedalboard = Pedalboard(info['title'])

        effects_instance = {}

        for effect_data in info['plugins']:
            effect = self._generate_effect(effect_data)
            pedalboard.append(effect)
            effects_instance[effect_data['instance']] = effect

        try:
            for connection_data in info['connections']:
                output_port = self._get_port(connection_data['source'], effects_instance, system_effect)
                input_port = self._get_port(connection_data['target'], effects_instance, system_effect)

                pedalboard.connect(output_port, input_port)
        except PortNotFoundError as e:
            if self.ignore_errors:
                print("WARNING:", e)
            else:
                raise e

        return pedalboard

    def _generate_effect(self, effect_data):
        effect = self.builder.build(effect_data['uri'])
        effect.active = not effect_data['bypassed']

        for param_data in effect_data['ports']:
            effect.params[param_data['symbol']].value = param_data['value']

        return effect

    def _get_port(self, name, effects_instance, system_effect):
        effect, port = self.filter_effect_port_symbol(name, effects_instance, system_effect)

        possible_ports = (effect.outputs, effect.midi_outputs, effect.inputs, effect.midi_inputs)
        filtered = filter(lambda ports: port in ports, possible_ports)

        ports = list(filtered)[0]
        return ports[port]

    def filter_effect_port_symbol(self, name, effects_instance, system_effect):
        if '/' in name:
            instance, port = name.split('/')
            effect = effects_instance[instance]
        elif self._is_system_effect(name, system_effect):
            effect = system_effect
            port = name
        else:
            raise PortNotFoundError("Port '{}' registered in system_effect?".format(name))

        return effect, port

    def _is_system_effect(self, name, system_effect):
        return name in system_effect.inputs or \
               name in system_effect.midi_inputs or \
               name in system_effect.outputs or \
               name in system_effect.midi_outputs

    def discover_system_effect(self, pedalboard_info):
        """
        Generate the system effect based in pedalboard_info

        :param dict pedalboard_info: For obtain this, see
            :meth:`~pluginsmanager.util.mod_pedalboard_converter.ModPedalboardConvert.get_pedalboard_info()`
        :return SystemEffect: SystemEffect generated based in pedalboard_info
        """
        # MOD swap ins and outs!!!
        hardware = pedalboard_info['hardware']

        total_audio_outs = hardware['audio_ins']
        total_audio_ins = hardware['audio_outs']

        outputs = ['capture_{}'.format(i) for i in range(1, total_audio_outs+1)]
        inputs = ['playback_{}'.format(i) for i in range(1, total_audio_ins+1)]

        midi_inputs = [
            'serial_midi_out' if hardware['serial_midi_out'] else midi_out['symbol']
            for midi_out in hardware['midi_outs'] if midi_out['valid']
        ]
        midi_outputs = [
            'serial_midi_in' if hardware['serial_midi_in'] else midi_in['symbol']
            for midi_in in hardware['midi_ins'] if midi_in['valid']
        ]

        return SystemEffect('system', outputs, inputs, midi_outputs, midi_inputs)
