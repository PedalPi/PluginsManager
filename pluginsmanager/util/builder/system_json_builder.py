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

from pluginsmanager.util.builder.builder import AudioPortBuilder


class SystemAudioPortBuilder(AudioPortBuilder):
    """
    Extracts the :class:`.SystemInput`s and :class:`.SystemOutputs`s of an :class:`.SystemEffect` defined in a json.
    """

    def __init__(self, system_effect):
        self.system_effect = system_effect

    def build_input(self, json):
        symbol = json['symbol']
        return self.system_effect.inputs[symbol]

    def build_output(self, json):
        symbol = json['symbol']
        return self.system_effect.outputs[symbol]

    def build_midi_input(self, json):
        symbol = json['symbol']
        return self.system_effect.midi_inputs[symbol]

    def build_midi_output(self, json):
        symbol = json['symbol']
        return self.system_effect.midi_outputs[symbol]
