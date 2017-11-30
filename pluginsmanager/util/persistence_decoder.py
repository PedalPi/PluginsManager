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

from pluginsmanager.model.bank import Bank
from pluginsmanager.model.lv2.lv2_effect_builder import Lv2EffectBuilder as Lv2LilvEffectBuilder
from pluginsmanager.model.pedalboard import Pedalboard
from pluginsmanager.util.builder.lv2_json_builder import Lv2AudioPortBuilder, Lv2EffectBuilder
from pluginsmanager.util.builder.system_json_builder import SystemAudioPortBuilder


class PersistenceDecoderError(Exception):
    pass


class PersistenceDecoder(object):

    def __init__(self, system_effect):
        self.system_effect = system_effect

    def read(self, json):
        reader = BankReader(self.system_effect)

        return reader.read(json)


class Reader(object):
    def __init__(self, system_effect):
        self.system_effect = system_effect

    def read(self, json):
        pass


class BankReader(Reader):

    def read(self, json):
        bank = Bank(json['name'])

        pedalboard_reader = PedalboardReader(self.system_effect)
        for pedalboard_json in json['pedalboards']:
            bank.append(pedalboard_reader.read(pedalboard_json))

        return bank


class PedalboardReader(Reader):

    def read(self, json):
        pedalboard = Pedalboard(json['name'])

        effect_reader = EffectReader(self.system_effect)
        for effect_json in json['effects']:
            pedalboard.append(effect_reader.read(effect_json))

        connection_reader = ConnectionReader(pedalboard, self.system_effect)
        for connection_json in json['connections']:
            port_output, port_input = connection_reader.read(connection_json)
            pedalboard.connect(port_output, port_input)

        if 'data' in json:
            pedalboard.data = json['data']

        return pedalboard


class EffectReader(Reader):

    def __init__(self, system_effect):
        super(EffectReader, self).__init__(system_effect)
        self.builder = Lv2LilvEffectBuilder()

    def read(self, json):
        return self.generate_builder(json).build(json)

    def generate_builder(self, json):
        technology = json['technology']

        if technology == 'lv2':
            return Lv2EffectBuilder(self.builder)
        else:
            raise PersistenceDecoderError('Unknown effect technology: ' + technology)


class ConnectionReader(Reader):

    def __init__(self, pedalboard, system_effect):
        super(ConnectionReader, self).__init__(system_effect)
        self.pedalboard = pedalboard

    def read(self, json):
        if json['type'] == 'audio':
            connection_output = self.generate_builder(json, 'output').build_output(json['output'])
            connection_input = self.generate_builder(json, 'input').build_input(json['input'])
        else:
            connection_output = self.generate_builder(json, 'output').build_midi_output(json['output'])
            connection_input = self.generate_builder(json, 'input').build_midi_input(json['input'])

        return connection_output, connection_input

    def generate_builder(self, json, audio_port):
        """
        :return AudioPortBuilder
        """
        if 'effect' in json[audio_port]:
            return Lv2AudioPortBuilder(self.pedalboard)
        else:
            return SystemAudioPortBuilder(self.system_effect)
