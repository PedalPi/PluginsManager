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


class MidiOutput(MidiPort, metaclass=ABCMeta):
    """
    MidiOutput is the medium in which the midi output processed
    by the effect is returned.

    For obtains the outputs::

        >>> cctonode
        <Lv2Effect object as 'CC2Note'  active at 0x7efe5480af28>
        >>> cctonode.outputs
        (<Lv2MidiOutput object as MIDI Out at 0x7efe5420eeb8>,)

        >>> midi_output = cctonode.midi_outputs[0]
        >>> midi_output
        <Lv2Output object as Out L at 0x7fd58c58a438>

        >>> symbol = midi_output.symbol
        >>> symbol
        'midiout'

        >>> cctonode.midi_outputs[symbol] == midi_output
        True

    For connections between effects, see :meth:`~pluginsmanager.model.pedalboard.Pedalboard.connect()`
    and :meth:`~pluginsmanager.model.pedalboard.Pedalboard.disconnect()` :class:`.Pedalboard` class methods.

    :param Effect effect: Effect that contains the output
    """

    @property
    def index(self):
        """
        :return: Output index in the your effect
        """
        return self.effect.midi_outputs.index(self)
