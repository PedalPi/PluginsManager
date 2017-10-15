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

from pluginsmanager.model.midi_output import MidiOutput


class Lv2MidiOutput(MidiOutput):
    """
    Representation of a Lv2 midi output port instance.

    For general input use, see :class:`.MidiOutput` and
    :class:`.Output` classes documentation.

    .. _output audio port: http://lv2plug.in/ns/lv2core/#OutputPort

    :param Lv2Effect effect: Effect that contains the midi output
    :param dict output: *midi output port* json representation
    """

    def __init__(self, effect, output):
        super(Lv2MidiOutput, self).__init__(effect)
        self._output = output

    def __str__(self):
        return self._output['name']

    @property
    def symbol(self):
        return self._output['symbol']

    @property
    def __dict__(self):
        dictionary = super(Lv2MidiOutput, self).__dict__
        dictionary['index'] = self._output['index']

        return dictionary
