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

from pluginsmanager.model.midi_input import MidiInput


class Lv2MidiInput(MidiInput):
    """
    Representation of a Lv2 midi input port instance.

    For general input use, see :class:`.MidiInput` and :class:`.Input` classes documentation.

    :param Lv2Effect effect: Effect that contains the midi input
    :param dict effect_midi_input: *midi input port* json representation
    """

    def __init__(self, effect, effect_midi_input):
        super(Lv2MidiInput, self).__init__(effect)
        self._input = effect_midi_input

    def __str__(self):
        return self._input['name']

    @property
    def symbol(self):
        return self._input['symbol']

    @property
    def __dict__(self):
        dictionary = super(Lv2MidiInput, self).__dict__
        dictionary['index'] = self._input['index']

        return dictionary
