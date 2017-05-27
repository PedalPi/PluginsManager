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

import unittest

from pluginsmanager.model.lv2.lv2_effect_builder import Lv2EffectBuilder
from pluginsmanager.model.connection import Connection
from pluginsmanager.model.system.system_effect import SystemEffect
from pluginsmanager.observer.mod_host.protocol_parser import ProtocolParser


class ProtocolParserTest(unittest.TestCase):
    builder = None

    @classmethod
    def setUpClass(cls):
        cls.builder = Lv2EffectBuilder()

    def test_add(self):
        effect_uri = 'http://calf.sourceforge.net/plugins/Reverb'
        effect_instance = 3

        reverb = self.builder.build(effect_uri)
        reverb.instance = effect_instance

        message = ProtocolParser.add(reverb)

        correct_message = "add {} {}".format(effect_uri, effect_instance)
        self.assertEqual(correct_message, message)

    def test_remove(self):
        effect_uri = 'http://calf.sourceforge.net/plugins/Reverb'
        effect_instance = 3

        reverb = self.builder.build(effect_uri)
        reverb.instance = effect_instance

        message = ProtocolParser.remove(reverb)

        correct_message = "remove {}".format(effect_instance)
        self.assertEqual(correct_message, message)

    def test_connect(self):
        effect1_instance = 3
        effect2_instance = 4

        reverb1 = self.builder.build('http://calf.sourceforge.net/plugins/Reverb')
        reverb2 = self.builder.build('http://calf.sourceforge.net/plugins/Reverb')
        reverb1.instance = effect1_instance
        reverb2.instance = effect2_instance

        output = reverb1.outputs[0]
        input = reverb2.inputs[0]
        connection = Connection(output, input)

        correct_message = 'connect effect_{}:{} effect_{}:{}'.format(
            reverb1.instance,
            output.symbol,
            reverb2.instance,
            input.symbol
        )

        self.assertEqual(correct_message, ProtocolParser.connect(connection))

    def test_connect_system_effect(self):
        system_effect = SystemEffect('system', ('capture_1', 'capture_2'), ('playback_1', 'playback_2'))

        output = system_effect.outputs[1]
        input = system_effect.inputs[0]
        connection = Connection(output, input)

        correct_message = 'connect system:{} system:{}'.format(
            output.symbol,
            input.symbol
        )

        self.assertEqual(correct_message, ProtocolParser.connect(connection))

    def test_disconnect(self):
        effect1_instance = 3
        effect2_instance = 4

        reverb1 = self.builder.build('http://calf.sourceforge.net/plugins/Reverb')
        reverb2 = self.builder.build('http://calf.sourceforge.net/plugins/Reverb')
        reverb1.instance = effect1_instance
        reverb2.instance = effect2_instance

        output = reverb1.outputs[0]
        input = reverb2.inputs[0]
        connection = Connection(output, input)

        correct_message = 'disconnect effect_{}:{} effect_{}:{}'.format(
            reverb1.instance,
            output.symbol,
            reverb2.instance,
            input.symbol
        )

        self.assertEqual(correct_message, ProtocolParser.disconnect(connection))

    @unittest.skip('Not implemented')
    def test_preset_load(self):
        assert False

    @unittest.skip('Not implemented')
    def test_preset_save(self):
        assert False

    @unittest.skip('Not implemented')
    def test_preset_show(self):
        assert False

    def test_param_set(self):
        effect_uri = 'http://calf.sourceforge.net/plugins/Reverb'
        effect_instance = 3

        reverb = self.builder.build(effect_uri)
        reverb.instance = effect_instance

        param = reverb.params[0]
        message = ProtocolParser.param_set(param)

        correct_message = "param_set {} {} {}".format(
            effect_instance,
            param.symbol,
            param.value
        )
        self.assertEqual(correct_message, message)

    def test_param_get(self):
        effect_uri = 'http://calf.sourceforge.net/plugins/Reverb'
        effect_instance = 3

        reverb = self.builder.build(effect_uri)
        reverb.instance = effect_instance

        param = reverb.params[0]
        message = ProtocolParser.param_get(param)

        correct_message = "param_get {} {}".format(
            effect_instance,
            param.symbol
        )
        self.assertEqual(correct_message, message)

    @unittest.skip('Not implemented')
    def test_param_monitor(self):
        assert False

    @unittest.skip('Not implemented')
    def test_monitor(self):
        assert False

    @unittest.skip('Not implemented')
    def test_midi_learn(self):
        assert False

    @unittest.skip('Not implemented')
    def test_midi_map(self):
        assert False

    @unittest.skip('Not implemented')
    def test_midi_unmap(self):
        assert False

    def test_bypass_effect_active(self):
        effect_uri = 'http://calf.sourceforge.net/plugins/Reverb'
        effect_instance = 3

        reverb = self.builder.build(effect_uri)
        reverb.instance = effect_instance
        reverb.active = True

        message = ProtocolParser.bypass(reverb)

        correct_message = "bypass {} {}".format(effect_instance, 1)
        self.assertEqual(correct_message, message)

    def test_bypass_effect_no_active(self):
        effect_uri = 'http://calf.sourceforge.net/plugins/Reverb'
        effect_instance = 3

        reverb = self.builder.build(effect_uri)
        reverb.instance = effect_instance
        reverb.active = False

        message = ProtocolParser.bypass(reverb)

        correct_message = "bypass {} {}".format(effect_instance, 0)
        self.assertEqual(correct_message, message)

    def test_load(self):
        filename = 'Não sei'
        correct_message = 'load {}'.format(filename)
        self.assertEqual(correct_message, ProtocolParser.load(filename))

    def test_save(self):
        filename = 'Não sei'
        correct_message = 'save {}'.format(filename)
        self.assertEqual(correct_message, ProtocolParser.save(filename))

    def test_help(self):
        self.assertEqual('help', ProtocolParser.help())

    def test_quit(self):
        self.assertEqual('quit', ProtocolParser.quit())

