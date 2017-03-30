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
from pluginsmanager.model.update_type import UpdateType
from pluginsmanager.model.updates_observer import UpdatesObserver


class Observer(UpdatesObserver):

    def on_bank_updated(self, bank, update_type, **kwargs):
        pass

    def on_pedalboard_updated(self, pedalboard, update_type, **kwargs):
        pass

    def on_effect_updated(self, effect, update_type, **kwargs):
        pass

    def on_effect_status_toggled(self, effect):
        pass

    def on_param_value_changed(self, param):
        pass

    def on_connection_updated(self, connection, update_type):
        pass


class UpdatesObserverTest(unittest.TestCase):

    def test_notify(self):
        observer1 = Observer()
        observer1.on_bank_updated = MagicMock()
        observer2 = Observer()
        observer2.on_bank_updated = MagicMock()
        observer3 = Observer()
        observer3.on_bank_updated = MagicMock()

        manager = BanksManager()
        manager.register(observer1)
        manager.register(observer2)
        manager.register(observer3)

        bank = Bank('Bank 1')
        with observer1:
            manager.banks.append(bank)

        observer1.on_bank_updated.assert_not_called()
        observer2.on_bank_updated.assert_called_with(bank, UpdateType.CREATED, index=0, origin=manager)
        observer3.on_bank_updated.assert_called_with(bank, UpdateType.CREATED, index=0, origin=manager)
