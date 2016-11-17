from pluginsmanager.model.bank import Bank
from pluginsmanager.model.patch import Patch
from pluginsmanager.model.connection import Connection

from pluginsmanager.model.lv2.lv2_effect_builder import Lv2EffectBuilder


class Persistance(object):

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

        patch_reader = PatchReader(self.system_effect)
        for patch_json in json['patches']:
            bank.append(patch_reader.read(patch_json))

        return bank

class PatchReader(Reader):

    def read(self, json):
        patch = Patch(json['name'])

        effect_reader = EffectReader(self.system_effect)
        for effect_json in json['effects']:
            patch.append(effect_reader.read(effect_json))

        connection_reader = ConnectionReader(patch, self.system_effect)
        for connection_json in json['connections']:
            patch.connections.append(connection_reader.read(connection_json))

        return patch

class EffectReader(Reader):

    def __init__(self, system_effect):
        super(EffectReader, self).__init__(system_effect)
        self.builder = Lv2EffectBuilder()

    def read(self, json):
        if json['technology'] == 'lv2':
            return self.read_lv2(json)

        raise Exception('Unkown effect technology: ' + json['technology'])

    def read_lv2(self, json):
        effect = self.builder.build(json['plugin'])

        for param, param_json in zip(effect.params, json['params']):
            param.value = param_json['value']

        effect.active = json['active']

        return effect

class ConnectionReader(Reader):

    def __init__(self, patch, system_effect):
        super(ConnectionReader, self).__init__(system_effect)
        self.patch = patch

    def read(self, json):
        if 'index' in json['output']:
            connection_output = self.read_output(json['output'])
        else:
            connection_output = self.read_system_output(json['output'])

        if 'index' in json['input']:
            connection_input = self.read_input(json['input'])
        else:
            connection_input = self.read_system_input(json['input'])

        return Connection(connection_output, connection_input)

    def read_output(self, json):
        index = json['symbol']

        effect_index = json['effect']
        effect = self.patch.effects[effect_index]

        return effect.outputs[index]

    def read_input(self, json):
        index = json['symbol']

        effect_index = json['effect']
        effect = self.patch.effects[effect_index]

        return effect.inputs[index]

    def read_system_output(self, json):
        return self.system_effect.outputs[json['symbol']]

    def read_system_input(self, json):
        return self.system_effect.inputs[json['symbol']]
