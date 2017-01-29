import unittest
from unittest.mock import MagicMock

from pluginsmanager.banks_manager import BanksManager

from pluginsmanager.model.bank import Bank
from pluginsmanager.model.pedalboard import Pedalboard

from pluginsmanager.model.lv2.lv2_effect_builder import Lv2EffectBuilder

from pluginsmanager.observer.autosaver import Autosaver


class AutoSaverTest(unittest.TestCase):

    def test_observers(self):
        mock = MagicMock()
        observer = Autosaver('test/data/')
        observer.save = mock
        observer.delete = mock

        manager = BanksManager()
        manager.register(observer)

        bank = Bank('Bank 1')
        manager.append(bank)
        observer.save.assert_called_with(bank)

        pedalboard = Pedalboard('Rocksmith')
        bank.append(pedalboard)
        observer.save.assert_called_with(bank)

        builder = Lv2EffectBuilder()
        reverb = builder.build('http://calf.sourceforge.net/plugins/Reverb')
        fuzz = builder.build('http://guitarix.sourceforge.net/plugins/gx_fuzzfacefm_#_fuzzfacefm_')
        reverb2 = builder.build('http://calf.sourceforge.net/plugins/Reverb')

        pedalboard.append(reverb)
        observer.save.assert_called_with(bank)
        pedalboard.append(fuzz)
        observer.save.assert_called_with(bank)
        pedalboard.append(reverb2)
        observer.save.assert_called_with(bank)

        reverb.outputs[0].connect(fuzz.inputs[0])
        observer.save.assert_called_with(bank)
        reverb.outputs[1].connect(fuzz.inputs[0])
        observer.save.assert_called_with(bank)
        fuzz.outputs[0].connect(reverb2.inputs[0])
        observer.save.assert_called_with(bank)
        reverb.outputs[0].connect(reverb2.inputs[0])
        observer.save.assert_called_with(bank)

        fuzz.toggle()
        observer.save.assert_called_with(bank)

        fuzz.params[0].value = fuzz.params[0].minimum / fuzz.params[0].maximum
        observer.save.assert_called_with(bank)

        del bank.pedalboards[0]
        observer.save.assert_called_with(bank)

        bank2 = Bank('Bank 2')
        manager.banks[0] = bank2
        observer.delete.assert_called_with(bank2)
        observer.save.assert_called_with(bank2)

        manager.banks.remove(bank2)
        observer.delete.assert_called_with(bank2)