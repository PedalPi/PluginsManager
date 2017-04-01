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
import os

from pluginsmanager.model.bank import Bank
from pluginsmanager.model.pedalboard import Pedalboard
from pluginsmanager.model.connection import Connection

from pluginsmanager.util.persistence_decoder import PersistenceDecoder, PersistenceDecoderError

from pluginsmanager.model.lv2.lv2_effect_builder import Lv2EffectBuilder
from pluginsmanager.model.system.system_effect import SystemEffect


class PersistenceTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.builder = Lv2EffectBuilder()

    @property
    def bank(self):
        sys_effect = SystemEffect('system', ('capture_1', 'capture_2'), ('playback_1', 'playback_2'))

        bank = Bank('Bank 1')
        pedalboard = Pedalboard('Pedalboard 1')

        bank.append(pedalboard)
        bank.append(Pedalboard('Pedalboard is a Pedalboard?'))

        reverb = self.builder.build('http://calf.sourceforge.net/plugins/Reverb')
        fuzz = self.builder.build('http://guitarix.sourceforge.net/plugins/gx_fuzzfacefm_#_fuzzfacefm_')
        reverb2 = self.builder.build('http://calf.sourceforge.net/plugins/Reverb')

        pedalboard.append(reverb)
        pedalboard.append(fuzz)
        pedalboard.append(reverb2)

        reverb.outputs[0].connect(fuzz.inputs[0])
        reverb.outputs[1].connect(fuzz.inputs[0])
        fuzz.outputs[0].connect(reverb2.inputs[0])
        reverb.outputs[0].connect(reverb2.inputs[0])

        pedalboard.connections.append(Connection(sys_effect.outputs[0], reverb.inputs[0]))
        pedalboard.connections.append(Connection(reverb2.outputs[0], sys_effect.inputs[0]))

        fuzz.toggle()
        fuzz.params[0].value = fuzz.params[0].minimum / fuzz.params[0].maximum

        return bank

    def test_read(self):
        system_effect = SystemEffect('system', ('capture_1', 'capture_2'), ('playback_1', 'playback_2'))

        util = PersistenceDecoder(system_effect)

        bank = self.bank
        bank_readed = util.read(bank.json)

        self.maxDiff = None
        self.assertEqual(bank.json, bank_readed.json)

    def test_read_unknown_technology(self):
        system_effect = SystemEffect('system', ('capture_1', 'capture_2'), ('playback_1', 'playback_2'))

        bank_data = {
            "index": 3, "name": "Bank 1",
            "pedalboards": [{
                "effects": [{"params": [{"index": 7, "symbol": "decay_time", "value": 1.5},
                                        {"index": 8, "symbol": "hf_damp", "value": 5000},
                                        {"index": 9, "symbol": "room_size", "value": 2},
                                        {"index": 10, "symbol": "diffusion", "value": 0.5},
                                        {"index": 11, "symbol": "amount", "value": 0.25},
                                        {"index": 12, "symbol": "dry", "value": 1},
                                        {"index": 13, "symbol": "predelay", "value": 0},
                                        {"index": 14, "symbol": "bass_cut", "value": 300},
                                        {"index": 15, "symbol": "treble_cut", "value": 5000}],
                "active": True, "technology": "ladspa",
                "plugin": "http://calf.sourceforge.net/plugins/Reverb"}],
            "name": "Pedalboard 1",
            "connections": []}]}

        with self.assertRaises(PersistenceDecoderError):
            PersistenceDecoder(system_effect).read(bank_data)

    @unittest.skip
    @unittest.skipIf('TRAVIS' in os.environ, 'Travis not contains audio interface')
    def test_read_system_builder(self):
        from pluginsmanager.model.system.system_effect_builder import SystemEffectBuilder

        system_effect = SystemEffectBuilder(False).build()

        util = PersistenceDecoder(system_effect)

        bank = self.bank
        bank_readed = util.read(bank.json)

        self.assertEqual(bank.json, bank_readed.json)
