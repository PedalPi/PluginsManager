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
from pluginsmanager.model.system.system_input import SystemInput
from pluginsmanager.model.system.system_output import SystemOutput

from pluginsmanager.util.dict_tuple import DictTuple


class SystemEffect(Effect):
    """
    Representation of the system instance (audio cards).

    System output is equivalent with audio input: You connect the
    instrument in the audio card input and it captures and send the
    audio to :class:`.SystemOutput` for you connect in a input plugins.

    System input is equivalent with audio output: The audio card receives
    the audio processed in your :class:`.SystemInput` and send it to audio
    card output for you connects in amplifier, headset.

    Because no autodetection of existing ports in audio card
    has been implemented, you must explicitly inform in the
    creation of the SystemEffect object::

    >>> sys_effect = SystemEffect('system', ('capture_1', 'capture_2'), ('playback_1', 'playback_2'))

    Unlike effects that should be added in the pedalboard, SystemEffects MUST NOT::

    >>> builder = Lv2EffectBuilder()

    >>> pedalboard = Pedalboard('Rocksmith')
    >>> reverb = builder.build('http://calf.sourceforge.net/plugins/Reverb')
    >>> pedalboard.append(reverb)

    However the pedalboard must have the connections::

    >>> pedalboard.connections.append(Connection(sys_effect.outputs[0], reverb.inputs[0]))

    An bypass example::

    >>> pedalboard = Pedalboard('Bypass example')
    >>> sys_effect = SystemEffect('system', ('capture_1', 'capture_2'), ('playback_1', 'playback_2'))
    >>> pedalboard.connections.append(Connection(sys_effect.outputs[0], sys_effect.inputs[0]))
    >>> pedalboard.connections.append(Connection(sys_effect.outputs[1], sys_effect.inputs[1]))

    :param string representation: Audio card representation. Usually 'system'
    :param tuple(string) outputs: Tuple of outputs representation. Usually a output representation
                                  starts with `capture_`
    :param tuple(string) inputs: Tuple of inputs representation. Usually a input representation
                                 starts with `playback_`
    """
    def __init__(self, representation, outputs, inputs):
        super(SystemEffect, self).__init__()

        self.representation = representation

        self._params = tuple()

        inputs = [SystemInput(self, effect_input) for effect_input in inputs]
        self._inputs = DictTuple(inputs, lambda _input: str(_input))

        outputs = [SystemOutput(self, effect_output) for effect_output in outputs]
        self._outputs = DictTuple(outputs, lambda _output: str(_output))

    def __str__(self):
        return self.representation

    def __repr__(self):
        return "<{} object as '{}' at 0x{:x}>".format(
            self.__class__.__name__,
            str(self),
            id(self)
        )

    @property
    def __dict__(self):
        return {
            'technology': 'system',
        }

    @property
    def is_possible_connect_itself(self):
        """
        return bool: Is possible connect the with it self?
        """
        return True
