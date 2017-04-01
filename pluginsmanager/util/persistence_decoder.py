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
from pluginsmanager.model.pedalboard import Pedalboard
from pluginsmanager.model.connection import Connection

from pluginsmanager.model.lv2.lv2_effect_builder import Lv2EffectBuilder


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
        bank.index = json['index']

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
            pedalboard.connections.append(connection_reader.read(connection_json))

        if 'data' in json:
            pedalboard.data = json['data']

        return pedalboard


class EffectReader(Reader):

    def __init__(self, system_effect):
        super(EffectReader, self).__init__(system_effect)
        self.builder = Lv2EffectBuilder()

    def read(self, json):
        if json['technology'] == 'lv2':
            return self.read_lv2(json)

        raise PersistenceDecoderError('Unknown effect technology: ' + json['technology'])

    def read_lv2(self, json):
        effect = self.builder.build(json['plugin'])

        for param, param_json in zip(effect.params, json['params']):
            param.value = param_json['value']

        effect.active = json['active']

        return effect


class ConnectionReader(Reader):

    def __init__(self, pedalboard, system_effect):
        super(ConnectionReader, self).__init__(system_effect)
        self.pedalboard = pedalboard

    def read(self, json):
        if 'effect' in json['output']:
            connection_output = self.read_output(json['output'])
        else:
            connection_output = self.read_system_output(json['output'])

        if 'effect' in json['input']:
            connection_input = self.read_input(json['input'])
        else:
            connection_input = self.read_system_input(json['input'])

        return Connection(connection_output, connection_input)

    def read_output(self, json):
        effect_index = json['effect']
        effect = self.pedalboard.effects[effect_index]

        return self.generic_system_output(effect, json['symbol'])

    def read_input(self, json):
        effect_index = json['effect']
        effect = self.pedalboard.effects[effect_index]

        return self.generic_system_input(effect, json['symbol'])

    def read_system_output(self, json):
        return self.generic_system_output(self.system_effect, json['symbol'])

    def read_system_input(self, json):
        return self.generic_system_input(self.system_effect, json['symbol'])

    def generic_system_output(self, effect, symbol):
        return effect.outputs[symbol]

    def generic_system_input(self, effect, symbol):
        return effect.inputs[symbol]
