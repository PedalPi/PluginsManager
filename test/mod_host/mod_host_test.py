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
from unittest.mock import MagicMock

import os

from pluginsmanager.banks_manager import BanksManager
from pluginsmanager.mod_host.mod_host import ModHost

from pluginsmanager.model.bank import Bank
from pluginsmanager.model.pedalboard import Pedalboard
from pluginsmanager.model.connection import Connection

from pluginsmanager.model.lv2.lv2_effect_builder import Lv2EffectBuilder

from pluginsmanager.model.system.system_effect import SystemEffect


class ModHostTest(unittest.TestCase):
    builder = None

    @classmethod
    def setUpClass(cls):
        cls.builder = Lv2EffectBuilder()

    @unittest.skip
    @unittest.skipIf('TRAVIS' in os.environ, 'Travis not contains audio interface')
    def test_observers(self):
        sys_effect = SystemEffect('system', ('capture_1', 'capture_2'), ('playback_1', 'playback_2'))
        manager = BanksManager()

        bank = Bank('Bank 1')
        manager.append(bank)

        mod_host = ModHost('localhost')
        mod_host.connect()
        manager.register(mod_host)

        pedalboard = Pedalboard('Rocksmith')

        mod_host.pedalboard = pedalboard

        bank.append(pedalboard)

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

        fuzz.toggle()
        fuzz.params[0].value = fuzz.params[0].minimum / fuzz.params[0].maximum

        fuzz.outputs[0].disconnect(reverb2.inputs[0])
        fuzz.toggle()

        pedalboard.effects.remove(fuzz)

        pedalboard.connections.append(Connection(sys_effect.outputs[0], reverb.inputs[0]))
        pedalboard.connections.append(Connection(reverb2.outputs[0], sys_effect.inputs[0]))

        for connection in list(pedalboard.connections):
            pedalboard.connections.remove(connection)

        for effect in list(pedalboard.effects):
            pedalboard.effects.remove(effect)

        #mod_host.auto_connect()

    def test_observers_mock(self):
        """Test only coverage"""
        sys_effect = SystemEffect('system', ('capture_1', 'capture_2'), ('playback_1', 'playback_2'))
        manager = BanksManager()

        bank = Bank('Bank 1')
        manager.append(bank)

        mod_host = ModHost('localhost')
        mod_host.host = MagicMock()
        manager.register(mod_host)

        pedalboard = Pedalboard('Rocksmith')

        mod_host.pedalboard = pedalboard

        bank.append(pedalboard)

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

        fuzz.toggle()
        fuzz.params[0].value = fuzz.params[0].minimum / fuzz.params[0].maximum

        fuzz.outputs[0].disconnect(reverb2.inputs[0])
        fuzz.toggle()

        pedalboard.effects.remove(fuzz)

        pedalboard.connections.append(Connection(sys_effect.outputs[0], reverb.inputs[0]))
        pedalboard.connections.append(Connection(reverb2.outputs[0], sys_effect.inputs[0]))

        for connection in list(pedalboard.connections):
            pedalboard.connections.remove(connection)

        for effect in list(pedalboard.effects):
            pedalboard.effects.remove(effect)

            # mod_host.auto_connect()

    def test_set_pedalboard(self):
        """Test only coverage"""
        manager = BanksManager()

        bank = Bank('Bank 1')
        manager.append(bank)

        mod_host = ModHost('localhost')
        mod_host.host = MagicMock()
        manager.register(mod_host)

        pedalboard = Pedalboard('test_set_pedalboard_1')
        bank.append(pedalboard)
        reverb = self.builder.build('http://calf.sourceforge.net/plugins/Reverb')
        pedalboard.append(reverb)

        pedalboard2 = Pedalboard('test_set_pedalboard_2')
        reverb2 = self.builder.build('http://calf.sourceforge.net/plugins/Reverb')
        bank.append(pedalboard)
        pedalboard2.append(reverb2)

        mod_host.pedalboard = pedalboard
        mod_host.pedalboard = pedalboard2

    def test_effect_status_not_current_pedalboard(self):
        """Test only coverage"""
        manager = BanksManager()

        bank = Bank('Bank 1')
        manager.append(bank)

        mod_host = ModHost('localhost')
        mod_host.host = MagicMock()
        manager.register(mod_host)

        pedalboard = Pedalboard('test_set_pedalboard_1')
        pedalboard.append(self.builder.build('http://calf.sourceforge.net/plugins/Reverb'))

        pedalboard2 = Pedalboard('test_set_pedalboard_2')
        pedalboard2.append(self.builder.build('http://calf.sourceforge.net/plugins/Reverb'))

        bank.append(pedalboard)
        bank.append(pedalboard2)

        mod_host.pedalboard = pedalboard

        pedalboard2.effects[0].toggle()

    def test_param_value_not_current_pedalboard(self):
        """Test only coverage"""
        manager = BanksManager()

        bank = Bank('Bank 1')
        manager.append(bank)

        mod_host = ModHost('localhost')
        mod_host.host = MagicMock()
        manager.register(mod_host)

        pedalboard = Pedalboard('test_set_pedalboard_1')
        pedalboard.append(self.builder.build('http://calf.sourceforge.net/plugins/Reverb'))

        pedalboard2 = Pedalboard('test_set_pedalboard_2')
        pedalboard2.append(self.builder.build('http://calf.sourceforge.net/plugins/Reverb'))

        bank.append(pedalboard)
        bank.append(pedalboard2)

        mod_host.pedalboard = pedalboard

        pedalboard2.effects[0].params[0].value = pedalboard2.effects[0].params[0].maximum

    def test_connection_not_current_pedalboard(self):
        """Test only coverage"""
        manager = BanksManager()

        bank = Bank('Bank 1')
        manager.append(bank)

        mod_host = ModHost('localhost')
        mod_host.host = MagicMock()
        manager.register(mod_host)

        pedalboard = Pedalboard('test_set_pedalboard_1')
        pedalboard.append(self.builder.build('http://calf.sourceforge.net/plugins/Reverb'))

        pedalboard2 = Pedalboard('test_set_pedalboard_2')
        pedalboard2.append(self.builder.build('http://calf.sourceforge.net/plugins/Reverb'))
        pedalboard2.append(self.builder.build('http://calf.sourceforge.net/plugins/Reverb'))

        bank.append(pedalboard)
        bank.append(pedalboard2)

        mod_host.pedalboard = pedalboard

        pedalboard2.effects[0].outputs[0].connect(pedalboard2.effects[1].inputs[0])
