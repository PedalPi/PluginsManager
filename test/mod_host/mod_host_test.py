import unittest
from unittest.mock import MagicMock

import os

from pluginsmanager.banks_manager import BanksManager
from pluginsmanager.mod_host.mod_host import ModHost

from pluginsmanager.model.bank import Bank
from pluginsmanager.model.patch import Patch
from pluginsmanager.model.connection import Connection

from pluginsmanager.model.lv2.lv2_effect_builder import Lv2EffectBuilder

from pluginsmanager.model.system.system_effect import SystemEffect


class PersistenceTest(unittest.TestCase):
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

        patch = Patch('Rocksmith')

        mod_host.patch = patch

        bank.append(patch)

        reverb = self.builder.build('http://calf.sourceforge.net/plugins/Reverb')
        fuzz = self.builder.build('http://guitarix.sourceforge.net/plugins/gx_fuzzfacefm_#_fuzzfacefm_')
        reverb2 = self.builder.build('http://calf.sourceforge.net/plugins/Reverb')

        patch.append(reverb)
        patch.append(fuzz)
        patch.append(reverb2)

        reverb.outputs[0].connect(fuzz.inputs[0])
        reverb.outputs[1].connect(fuzz.inputs[0])
        fuzz.outputs[0].connect(reverb2.inputs[0])
        reverb.outputs[0].connect(reverb2.inputs[0])

        fuzz.toggle()
        fuzz.params[0].value = fuzz.params[0].minimum / fuzz.params[0].maximum

        fuzz.outputs[0].disconnect(reverb2.inputs[0])
        fuzz.toggle()

        patch.effects.remove(fuzz)

        patch.connections.append(Connection(sys_effect.outputs[0], reverb.inputs[0]))
        patch.connections.append(Connection(reverb2.outputs[0], sys_effect.inputs[0]))

        for connection in list(patch.connections):
            patch.connections.remove(connection)

        for effect in list(patch.effects):
            patch.effects.remove(effect)

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

        patch = Patch('Rocksmith')

        mod_host.patch = patch

        bank.append(patch)

        reverb = self.builder.build('http://calf.sourceforge.net/plugins/Reverb')
        fuzz = self.builder.build('http://guitarix.sourceforge.net/plugins/gx_fuzzfacefm_#_fuzzfacefm_')
        reverb2 = self.builder.build('http://calf.sourceforge.net/plugins/Reverb')

        patch.append(reverb)
        patch.append(fuzz)
        patch.append(reverb2)

        reverb.outputs[0].connect(fuzz.inputs[0])
        reverb.outputs[1].connect(fuzz.inputs[0])
        fuzz.outputs[0].connect(reverb2.inputs[0])
        reverb.outputs[0].connect(reverb2.inputs[0])

        fuzz.toggle()
        fuzz.params[0].value = fuzz.params[0].minimum / fuzz.params[0].maximum

        fuzz.outputs[0].disconnect(reverb2.inputs[0])
        fuzz.toggle()

        patch.effects.remove(fuzz)

        patch.connections.append(Connection(sys_effect.outputs[0], reverb.inputs[0]))
        patch.connections.append(Connection(reverb2.outputs[0], sys_effect.inputs[0]))

        for connection in list(patch.connections):
            patch.connections.remove(connection)

        for effect in list(patch.effects):
            patch.effects.remove(effect)

            # mod_host.auto_connect()

    def test_set_patch(self):
        """Test only coverage"""
        manager = BanksManager()

        bank = Bank('Bank 1')
        manager.append(bank)

        mod_host = ModHost('localhost')
        mod_host.host = MagicMock()
        manager.register(mod_host)

        patch = Patch('test_set_patch_1')
        bank.append(patch)
        reverb = self.builder.build('http://calf.sourceforge.net/plugins/Reverb')
        patch.append(reverb)

        patch2 = Patch('test_set_patch_2')
        reverb2 = self.builder.build('http://calf.sourceforge.net/plugins/Reverb')
        bank.append(patch)
        patch2.append(reverb2)

        mod_host.patch = patch
        mod_host.patch = patch2

    def test_effect_status_not_current_patch(self):
        """Test only coverage"""
        manager = BanksManager()

        bank = Bank('Bank 1')
        manager.append(bank)

        mod_host = ModHost('localhost')
        mod_host.host = MagicMock()
        manager.register(mod_host)

        patch = Patch('test_set_patch_1')
        patch.append(self.builder.build('http://calf.sourceforge.net/plugins/Reverb'))

        patch2 = Patch('test_set_patch_2')
        patch2.append(self.builder.build('http://calf.sourceforge.net/plugins/Reverb'))

        bank.append(patch)
        bank.append(patch2)

        mod_host.patch = patch

        patch2.effects[0].toggle()

    def test_param_value_not_current_patch(self):
        """Test only coverage"""
        manager = BanksManager()

        bank = Bank('Bank 1')
        manager.append(bank)

        mod_host = ModHost('localhost')
        mod_host.host = MagicMock()
        manager.register(mod_host)

        patch = Patch('test_set_patch_1')
        patch.append(self.builder.build('http://calf.sourceforge.net/plugins/Reverb'))

        patch2 = Patch('test_set_patch_2')
        patch2.append(self.builder.build('http://calf.sourceforge.net/plugins/Reverb'))

        bank.append(patch)
        bank.append(patch2)

        mod_host.patch = patch

        patch2.effects[0].params[0].value = patch2.effects[0].params[0].maximum

    def test_connection_not_current_patch(self):
        """Test only coverage"""
        manager = BanksManager()

        bank = Bank('Bank 1')
        manager.append(bank)

        mod_host = ModHost('localhost')
        mod_host.host = MagicMock()
        manager.register(mod_host)

        patch = Patch('test_set_patch_1')
        patch.append(self.builder.build('http://calf.sourceforge.net/plugins/Reverb'))

        patch2 = Patch('test_set_patch_2')
        patch2.append(self.builder.build('http://calf.sourceforge.net/plugins/Reverb'))
        patch2.append(self.builder.build('http://calf.sourceforge.net/plugins/Reverb'))

        bank.append(patch)
        bank.append(patch2)

        mod_host.patch = patch

        patch2.effects[0].outputs[0].connect(patch2.effects[1].inputs[0])
