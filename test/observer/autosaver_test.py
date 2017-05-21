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

from pluginsmanager.banks_manager import BanksManager

from pluginsmanager.model.bank import Bank
from pluginsmanager.model.pedalboard import Pedalboard

from pluginsmanager.model.lv2.lv2_effect_builder import Lv2EffectBuilder

from pluginsmanager.observer.autosaver.autosaver import Autosaver


class AutoSaverTest(unittest.TestCase):

    def autosaver(self, auto_save=True):
        return Autosaver('../data/autosaver_data/', auto_save=auto_save)

    def test_observers(self):
        save_mock = MagicMock()
        delete_mock = MagicMock()

        observer = self.autosaver()
        observer.banks_files.save_bank = save_mock
        observer.banks_files.delete_bank = delete_mock

        manager = BanksManager()
        manager.register(observer)

        bank = Bank('Bank 1')
        manager.append(bank)
        save_mock.assert_called_with(bank)
        save_mock.reset_mock()

        pedalboard = Pedalboard('Rocksmith')
        bank.append(pedalboard)
        save_mock.assert_called_with(bank)
        save_mock.reset_mock()

        builder = Lv2EffectBuilder()
        reverb = builder.build('http://calf.sourceforge.net/plugins/Reverb')
        filter = builder.build('http://calf.sourceforge.net/plugins/Filter')
        reverb2 = builder.build('http://calf.sourceforge.net/plugins/Reverb')

        pedalboard.append(reverb)
        save_mock.assert_called_with(bank)
        save_mock.reset_mock()
        pedalboard.append(filter)
        save_mock.assert_called_with(bank)
        save_mock.reset_mock()
        pedalboard.append(reverb2)
        save_mock.assert_called_with(bank)
        save_mock.reset_mock()

        reverb.outputs[0].connect(filter.inputs[0])
        save_mock.assert_called_with(bank)
        save_mock.reset_mock()
        reverb.outputs[1].connect(filter.inputs[0])
        save_mock.assert_called_with(bank)
        save_mock.reset_mock()
        filter.outputs[0].connect(reverb2.inputs[0])
        save_mock.assert_called_with(bank)
        save_mock.reset_mock()
        reverb.outputs[0].connect(reverb2.inputs[0])
        save_mock.assert_called_with(bank)
        save_mock.reset_mock()

        filter.toggle()
        save_mock.assert_called_with(bank)
        save_mock.reset_mock()

        filter.params[0].value = (filter.params[0].maximum - filter.params[0].minimum) / 2
        save_mock.assert_called_with(bank)
        save_mock.reset_mock()

        del bank.pedalboards[0]
        save_mock.assert_called_with(bank)
        save_mock.reset_mock()

        bank2 = Bank('Bank 2')
        manager.banks[0] = bank2
        delete_mock.assert_called_with(bank)
        save_mock.assert_called_with(bank2)

        delete_mock.reset_mock()
        save_mock.reset_mock()

        manager.banks.remove(bank2)
        delete_mock.assert_called_with(bank2)
        delete_mock.reset_mock()

    def test_replace_bank(self):
        observer = self.autosaver()

        manager = BanksManager()
        manager.register(observer)

        bank1 = Bank('Bank 1')
        pedalboard = Pedalboard('Rocksmith')
        bank1.append(pedalboard)

        manager.append(bank1)

        manager.banks[0] = Bank('Bank 2')

        self.validate_persisted(manager)

        while manager.banks:
            del manager.banks[0]

    def test_swap_bank(self):
        observer = self.autosaver()

        manager = BanksManager()
        manager.register(observer)

        bank1 = Bank('Bank 1')
        bank2 = Bank('Bank 2')

        manager.append(bank1)
        manager.append(bank2)

        manager.banks[0], manager.banks[1] = manager.banks[1], manager.banks[0]

        self.validate_persisted(manager)

        while manager.banks:
            del manager.banks[0]

    def validate_persisted(self, manager):
        autosaver_validation = self.autosaver()
        banks_manager = autosaver_validation.load(None)

        self.assertEqual(len(manager.banks), len(banks_manager.banks))

        for bank_manager, bank_persisted in zip(manager.banks, banks_manager.banks):
            self.assertEqual(bank_manager.json, bank_persisted.json)

    def test_manual_save(self):
        observer = self.autosaver(auto_save=False)

        manager = BanksManager()
        manager.register(observer)

        bank1 = Bank('Bank 1')
        bank2 = Bank('Bank 2')

        manager.append(bank1)
        manager.append(bank2)

        # Not saved
        self.assertEqual(0, len(self.autosaver().load(None).banks))

        # Now has saved
        observer.save(manager)
        self.validate_persisted(manager)

        while manager.banks:
            manager.banks.pop()

        # Not saved
        self.assertEqual(2, len(self.autosaver().load(None).banks))

        # Now has saved
        observer.save(manager)
        self.validate_persisted(manager)
