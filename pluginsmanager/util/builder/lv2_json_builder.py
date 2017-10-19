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
from pluginsmanager.util.builder.builder import AudioPortBuilder, EffectBuilder


class Lv2AudioPortBuilder(AudioPortBuilder):
    """
    Extracts the :class:`.Lv2Input`s and :class:`.Lv2Outputs`s of an :class:`.Lv2Effect` defined in a json.
    """

    def __init__(self, pedalboard):
        self.pedalboard = pedalboard

    def build_input(self, json):
        symbol = json['symbol']
        return self.get_effect(json).inputs[symbol]

    def build_output(self, json):
        symbol = json['symbol']
        return self.get_effect(json).outputs[symbol]

    def build_midi_input(self, json):
        symbol = json['symbol']
        return self.get_effect(json).midi_inputs[symbol]

    def build_midi_output(self, json):
        symbol = json['symbol']
        return self.get_effect(json).midi_outputs[symbol]

    def get_effect(self, json):
        effect_index = json['effect']
        return self.pedalboard.effects[effect_index]


class Lv2EffectBuilder(EffectBuilder):
    def __init__(self, lv2_effect_builder):
        """
        :param model.lv2.lv2_effect_builder.Lv2EffectBuilder lv2_effect_builder:
        """
        self.builder = lv2_effect_builder

    def build(self, json):
        effect = self.builder.build(json['plugin'])

        for param, param_json in zip(effect.params, json['params']):
            param.value = param_json['value']

        effect.active = json['active']

        return effect
