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

from abc import ABCMeta

from pluginsmanager.model.midi_port import MidiPort


class MidiInput(MidiPort, metaclass=ABCMeta):
    """
    MidiInput is the medium in which the midi input port will go into
    effect to be processed.

    For obtains the inputs::

        >>> cctonode
        <Lv2Effect object as 'CC2Note'  active at 0x7efe5480af28>
        >>> cctonode.midi_inputs
        (<Lv2MidiInput object as MIDI In at 0x7efe54535dd8>,)

        >>> midi_input = cctonode.midi_inputs[0]
        >>> midi_input
        <Lv2MidiInput object as MIDI In at 0x7efe54535dd8>

        >>> symbol = midi_input.symbol
        >>> symbol
        'midiin'

        >>> cctonode.midi_inputs[symbol] == midi_input
        True

    For connections between effects, see :meth:`~pluginsmanager.model.pedalboard.Pedalboard.connect()`
    and :meth:`~pluginsmanager.model.pedalboard.Pedalboard.disconnect()` :class:`.Pedalboard` class methods.

    :param Effect effect: Effect of midi input
    """

    @property
    def index(self):
        """
        :return: MidiInput index in the your effect
        """
        return self.effect.midi_inputs.index(self)
