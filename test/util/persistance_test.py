import unittest
import os

from pluginsmanager.model.bank import Bank
from pluginsmanager.model.patch import Patch
from pluginsmanager.model.connection import Connection

from pluginsmanager.util.persistance import Persistance

from pluginsmanager.model.lv2.lv2_effect_builder import Lv2EffectBuilder
from pluginsmanager.model.system.system_effect_builder import SystemEffectBuilder
from pluginsmanager.model.system.system_effect import SystemEffect


class ObservableListTest(unittest.TestCase):

    @property
    def bank(self):
        sys_effect = SystemEffect('system', ('capture_1', 'capture_2'), ('playback_1', 'playback_2'))

        bank = Bank('Bank 1')
        bank.index = 3

        patch = Patch('Patch 1')

        bank.append(patch)
        bank.append(Patch('Pedalboard is a Patch?'))

        builder = Lv2EffectBuilder()
        reverb = builder.build('http://calf.sourceforge.net/plugins/Reverb')
        fuzz = builder.build('http://guitarix.sourceforge.net/plugins/gx_fuzzfacefm_#_fuzzfacefm_')
        reverb2 = builder.build('http://calf.sourceforge.net/plugins/Reverb')

        patch.append(reverb)
        patch.append(fuzz)
        patch.append(reverb2)

        reverb.outputs[0].connect(fuzz.inputs[0])
        reverb.outputs[1].connect(fuzz.inputs[0])
        fuzz.outputs[0].connect(reverb2.inputs[0])
        reverb.outputs[0].connect(reverb2.inputs[0])

        patch.connections.append(Connection(sys_effect.outputs[0], reverb.inputs[0]))
        patch.connections.append(Connection(reverb2.outputs[0], sys_effect.inputs[0]))

        fuzz.toggle()
        fuzz.params[0].value = fuzz.params[0].minimum / fuzz.params[0].maximum

        return bank

    def test_read(self):
        system_effect = SystemEffect('system', ('capture_1', 'capture_2'), ('playback_1', 'playback_2'))

        util = Persistance(system_effect)

        bank = self.bank
        bank_readed = util.read(bank.json)

        self.assertEqual(bank.json, bank_readed.json)

    @unittest.skipIf('TRAVIS' in os.environ, 'Travis not contains audio interface')
    def test_read(self):
        system_effect = SystemEffectBuilder(False).build()

        util = Persistance(system_effect)

        bank = self.bank
        bank_readed = util.read(bank.json)

        self.assertEqual(bank.json, bank_readed.json)
