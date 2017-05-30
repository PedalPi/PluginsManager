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
from unittest.mock import MagicMock, call

from pluginsmanager.banks_manager import BanksManager
from pluginsmanager.model.bank import Bank
from pluginsmanager.model.connection import Connection
from pluginsmanager.model.lv2.lv2_effect_builder import Lv2EffectBuilder
from pluginsmanager.model.pedalboard import Pedalboard
from pluginsmanager.observer.update_type import UpdateType


class BanksManagerTest(unittest.TestCase):

    def test_observers_calls(self):
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
        filter = builder.build('http://calf.sourceforge.net/plugins/Filter')
        reverb2 = builder.build('http://calf.sourceforge.net/plugins/Reverb')

        pedalboard.append(reverb)
        observer.on_effect_updated.assert_called_with(reverb, UpdateType.CREATED, index=reverb.index, origin=pedalboard)
        pedalboard.append(filter)
        observer.on_effect_updated.assert_called_with(filter, UpdateType.CREATED, index=filter.index, origin=pedalboard)
        pedalboard.append(reverb2)
        observer.on_effect_updated.assert_called_with(reverb2, UpdateType.CREATED, index=reverb2.index, origin=pedalboard)

        reverb.outputs[0].connect(filter.inputs[0])
        observer.on_connection_updated.assert_called_with(
            Connection(reverb.outputs[0], filter.inputs[0]),
            UpdateType.CREATED,
            pedalboard=pedalboard
        )
        reverb.outputs[1].connect(filter.inputs[0])
        observer.on_connection_updated.assert_called_with(
            Connection(reverb.outputs[1], filter.inputs[0]),
            UpdateType.CREATED,
            pedalboard=pedalboard
        )
        filter.outputs[0].connect(reverb2.inputs[0])
        observer.on_connection_updated.assert_called_with(
            Connection(filter.outputs[0], reverb2.inputs[0]),
            UpdateType.CREATED,
            pedalboard=pedalboard
        )
        reverb.outputs[0].connect(reverb2.inputs[0])
        observer.on_connection_updated.assert_called_with(
            Connection(reverb.outputs[0], reverb2.inputs[0]),
            UpdateType.CREATED,
            pedalboard=pedalboard
        )

        filter.toggle()
        observer.on_effect_status_toggled.assert_called_with(filter)

        filter.params[0].value = (filter.params[0].maximum - filter.params[0].minimum) / 2
        observer.on_param_value_changed.assert_called_with(filter.params[0])

        del bank.pedalboards[0]
        observer.on_pedalboard_updated.assert_called_with(pedalboard, UpdateType.DELETED, index=0, origin=bank)

        bank2 = Bank('Bank 2')
        old_bank = manager.banks[0]
        manager.banks[0] = bank2
        observer.on_bank_updated.assert_called_with(bank2, UpdateType.UPDATED, index=0, origin=manager, old=old_bank)

        manager.banks.remove(bank2)
        observer.on_bank_updated.assert_called_with(bank2, UpdateType.DELETED, index=0, origin=manager)

    def test_initial_banks(self):
        banks = [Bank('Bank 1'), Bank('Bank 1')]

        manager = BanksManager(banks)

        for original_bank, bank_managed in zip(banks, manager.banks):
            self.assertEqual(original_bank, bank_managed)

    def test_swap_banks(self):
        manager = BanksManager()

        bank1 = Bank('Bank 1')
        bank2 = Bank('Bank 2')
        bank3 = Bank('Bank 3')
        bank4 = Bank('Bank 4')

        manager.append(bank1)
        manager.append(bank2)
        manager.append(bank3)
        manager.append(bank4)

        observer = MagicMock()
        manager.register(observer)

        manager.banks[1], manager.banks[3] = manager.banks[3], manager.banks[1]

        calls = [
            call(bank4, UpdateType.UPDATED, index=1, origin=manager, old=bank2),
            call(bank2, UpdateType.UPDATED, index=3, origin=manager, old=bank4)
        ]

        self.assertListEqual(calls, observer.on_bank_updated.call_args_list)

        self.assertEqual(bank2.manager, manager)
        self.assertEqual(bank4.manager, manager)

    def test_observers(self):
        observer1 = MagicMock()
        observer2 = MagicMock()

        manager = BanksManager()

        manager.register(observer1)
        manager.register(observer2)

        self.assertListEqual([observer1, observer2], manager.observers)
