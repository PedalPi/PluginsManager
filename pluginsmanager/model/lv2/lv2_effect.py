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

from pluginsmanager.model.effect import Effect
from pluginsmanager.model.lv2.lv2_param import Lv2Param
from pluginsmanager.model.lv2.lv2_input import Lv2Input
from pluginsmanager.model.lv2.lv2_output import Lv2Output
from pluginsmanager.model.lv2.lv2_midi_input import Lv2MidiInput
from pluginsmanager.model.lv2.lv2_midi_output import Lv2MidiOutput

from pluginsmanager.util.dict_tuple import DictTuple


class Lv2Effect(Effect):
    """
    Representation of a Lv2 audio plugin instance.

    For general effect use, see :class:`.Effect` class documentation.

    It's possible obtains the :class:`.Lv2Plugin` information::

        >>> reverb
        <Lv2Effect object as 'Calf Reverb'  active at 0x7f60effb09e8>
        >>> reverb.plugin
        <Lv2Plugin object as Calf Reverb at 0x7f60effb9940>

    :param Lv2Plugin plugin:
    """

    def __init__(self, plugin):
        super(Lv2Effect, self).__init__()

        self.plugin = plugin

        params = [Lv2Param(self, param) for param in plugin["ports"]["control"]["input"]]
        self._params = DictTuple(params, lambda param: param.symbol)

        inputs = [Lv2Input(self, effect_input) for effect_input in plugin['ports']['audio']['input']]
        self._inputs = DictTuple(inputs, lambda _input: _input.symbol)

        outputs = [Lv2Output(self, effect_output) for effect_output in plugin['ports']['audio']['output']]
        self._outputs = DictTuple(outputs, lambda _output: _output.symbol)

        midi_inputs = [Lv2MidiInput(self, midi_input) for midi_input in plugin['ports']['midi']['input']]
        self._midi_inputs = DictTuple(midi_inputs, lambda _output: _output.symbol)

        midi_outputs = [Lv2MidiOutput(self, midi_output) for midi_output in plugin['ports']['midi']['output']]
        self._midi_outputs = DictTuple(midi_outputs, lambda _output: _output.symbol)

        self.instance = None

    def __str__(self):
        return str(self.plugin)

    def __repr__(self):
        return "<{} object as '{}' {} active at 0x{:x}>".format(
            self.__class__.__name__,
            str(self),
            '' if self.active else 'not',
            id(self)
        )

    @property
    def __dict__(self):
        return {
            'technology': 'lv2',
            'plugin': self.plugin['uri'],
            'active': self.active,
            'params': [param.json for param in self.params],
            'version': self.version
        }

    @property
    def version(self):
        """
        :return string: Version of plugin of effect
        """
        return self.plugin.version
