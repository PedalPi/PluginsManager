import unittest
from unittest.mock import MagicMock

from pluginsmanager.banks_manager import BanksManager

from pluginsmanager.model.bank import Bank
from pluginsmanager.model.connection import Connection
from pluginsmanager.model.pedalboard import Pedalboard
from pluginsmanager.model.update_type import UpdateType

from pluginsmanager.model.lv2.lv2_effect_builder import Lv2EffectBuilder


class BanksManagerTest(unittest.TestCase):

    def test_observers(self):
        observer = MagicMock()

        manager = BanksManager()
        manager.register(observer)

        bank = Bank('Bank 1')
        manager.append(bank)
        observer.on_bank_updated.assert_called_with(bank, UpdateType.CREATED, index=0, origin=manager)

        pedalboard = Pedalboard('Rocksmith')
        bank.append(pedalboard)
        observer.on_pedalboard_updated.assert_called_with(pedalboard, UpdateType.CREATED, index=0, origin=bank)

        builder = Lv2EffectBuilder()
        reverb = builder.build('http://calf.sourceforge.net/plugins/Reverb')
        fuzz = builder.build('http://guitarix.sourceforge.net/plugins/gx_fuzzfacefm_#_fuzzfacefm_')
        reverb2 = builder.build('http://calf.sourceforge.net/plugins/Reverb')

        pedalboard.append(reverb)
        observer.on_effect_updated.assert_called_with(reverb, UpdateType.CREATED)
        pedalboard.append(fuzz)
        observer.on_effect_updated.assert_called_with(fuzz, UpdateType.CREATED)
        pedalboard.append(reverb2)
        observer.on_effect_updated.assert_called_with(reverb2, UpdateType.CREATED)

        reverb.outputs[0].connect(fuzz.inputs[0])
        observer.on_connection_updated.assert_called_with(
            Connection(reverb.outputs[0], fuzz.inputs[0]),
            UpdateType.CREATED,
        )
        reverb.outputs[1].connect(fuzz.inputs[0])
        observer.on_connection_updated.assert_called_with(
            Connection(reverb.outputs[1], fuzz.inputs[0]),
            UpdateType.CREATED,
        )
        fuzz.outputs[0].connect(reverb2.inputs[0])
        observer.on_connection_updated.assert_called_with(
            Connection(fuzz.outputs[0], reverb2.inputs[0]),
            UpdateType.CREATED,
        )
        reverb.outputs[0].connect(reverb2.inputs[0])
        observer.on_connection_updated.assert_called_with(
            Connection(reverb.outputs[0], reverb2.inputs[0]),
            UpdateType.CREATED,
        )

        fuzz.toggle()
        observer.on_effect_status_toggled.assert_called_with(fuzz)

        fuzz.params[0].value = fuzz.params[0].minimum / fuzz.params[0].maximum
        observer.on_param_value_changed.assert_called_with(fuzz.params[0])

        del bank.pedalboards[0]
        observer.on_pedalboard_updated.assert_called_with(pedalboard, UpdateType.DELETED, index=0, origin=bank)

        bank2 = Bank('Bank 2')
        manager.banks[0] = bank2
        observer.on_bank_updated.assert_called_with(bank2, UpdateType.UPDATED, index=0, origin=manager)

        manager.banks.remove(bank2)
        observer.on_bank_updated.assert_called_with(bank2, UpdateType.DELETED, index=0, origin=manager)

    def test_initial_banks(self):
        banks = [Bank('Bank 1'), Bank('Bank 1')]

        manager = BanksManager(banks)

        for original_bank, bank_managed in zip(banks, manager.banks):
            self.assertEqual(original_bank, bank_managed)
