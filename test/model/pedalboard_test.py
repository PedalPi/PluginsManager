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

from pluginsmanager.model.bank import Bank
from pluginsmanager.model.effects_list import NotAddableError
from pluginsmanager.model.lv2.lv2_effect_builder import Lv2EffectBuilder
from pluginsmanager.model.pedalboard import Pedalboard
from pluginsmanager.model.system.system_effect import SystemEffect
from pluginsmanager.observer.update_type import UpdateType, CustomChange


class PedalboardTest(unittest.TestCase):

    @property
    def mock_effect(self):
        effect = MagicMock()
        effect.is_unique_for_all_pedalboards = False
        return effect

    def test_add_effect_by_effects(self):
        pedalboard = Pedalboard('Pedalboard 1')

        effect1 = self.mock_effect
        effect2 = self.mock_effect

        pedalboard.observer = MagicMock()

        pedalboard.effects.append(effect1)
        self.assertEqual(effect1.pedalboard, pedalboard)
        self.assertEqual(pedalboard.effects[0], effect1)
        pedalboard.observer.on_effect_updated.assert_called_with(effect1, UpdateType.CREATED, index=0, origin=pedalboard)

        pedalboard.effects.append(effect2)
        self.assertEqual(effect2.pedalboard, pedalboard)
        self.assertEqual(pedalboard.effects[1], effect2)
        pedalboard.observer.on_effect_updated.assert_called_with(effect2, UpdateType.CREATED, index=1, origin=pedalboard)

    def test_add_effect(self):
        pedalboard = Pedalboard('Pedalboard 1')

        effect1 = self.mock_effect
        effect2 = self.mock_effect

        pedalboard.observer = MagicMock()

        pedalboard.append(effect1)
        self.assertEqual(effect1.pedalboard, pedalboard)
        self.assertEqual(pedalboard.effects[0], effect1)
        pedalboard.observer.on_effect_updated.assert_called_with(effect1, UpdateType.CREATED, index=0, origin=pedalboard)

        pedalboard.append(effect2)
        self.assertEqual(effect2.pedalboard, pedalboard)
        self.assertEqual(pedalboard.effects[1], effect2)
        pedalboard.observer.on_effect_updated.assert_called_with(effect2, UpdateType.CREATED, index=1, origin=pedalboard)

    def test_update_effect(self):
        pedalboard = Pedalboard('Pedalboard 1')

        effect1 = self.mock_effect
        effect2 = self.mock_effect

        pedalboard.append(effect1)

        pedalboard.observer = MagicMock()
        pedalboard.effects[0] = effect2

        self.assertEqual(effect1.pedalboard, None)
        self.assertEqual(effect2.pedalboard, pedalboard)
        self.assertEqual(pedalboard.effects[0], effect2)
        pedalboard.observer.on_effect_updated.assert_called_with(effect2, UpdateType.UPDATED, index=0, origin=pedalboard)

    def test_delete_effect(self):
        pedalboard = Pedalboard('Bank 1')

        effect = self.mock_effect
        effect2 = self.mock_effect

        pedalboard.append(effect)
        pedalboard.append(effect2)

        pedalboard.observer = MagicMock()
        del pedalboard.effects[1]

        self.assertEqual(effect2.pedalboard, None)
        self.assertEqual(len(pedalboard.effects), 1)
        pedalboard.observer.on_effect_updated.assert_called_with(effect2, UpdateType.DELETED, index=1, origin=pedalboard)

        del pedalboard.effects[0]
        self.assertEqual(effect.pedalboard, None)
        self.assertEqual(len(pedalboard.effects), 0)
        pedalboard.observer.on_effect_updated.assert_called_with(effect, UpdateType.DELETED, index=0, origin=pedalboard)

    def test_add_connection_by_connections(self):
        """ Other mode is by output.connect(input)"""
        pedalboard = Pedalboard('Pedalboard 1')

        connection1 = MagicMock()
        connection2 = MagicMock()

        pedalboard.observer = MagicMock()

        pedalboard.connections.append(connection1)
        self.assertEqual(pedalboard.connections[0], connection1)
        pedalboard.observer.on_connection_updated.assert_called_with(connection1, UpdateType.CREATED, pedalboard=pedalboard)

        pedalboard.connections.append(connection2)
        self.assertEqual(pedalboard.connections[1], connection2)
        pedalboard.observer.on_connection_updated.assert_called_with(connection2, UpdateType.CREATED, pedalboard=pedalboard)

    def test_update_connection(self):
        pedalboard = Pedalboard('Pedalboard 1')

        connection1 = MagicMock()
        connection2 = MagicMock()

        pedalboard.connections.append(connection1)

        pedalboard.observer = MagicMock()
        pedalboard.connections[0] = connection2

        self.assertEqual(pedalboard.connections[0], connection2)
        pedalboard.observer.on_connection_updated.assert_called_with(connection2, UpdateType.UPDATED, pedalboard=pedalboard, old=connection1)

    def test_delete_connection(self):
        """ Other mode is by output.disconnect(input)"""
        pedalboard = Pedalboard('Bank 1')

        connection = MagicMock()

        pedalboard.connections.append(connection)

        pedalboard.observer = MagicMock()
        del pedalboard.connections[0]

        self.assertEqual(len(pedalboard.connections), 0)
        pedalboard.observer.on_connection_updated.assert_called_with(connection, UpdateType.DELETED, pedalboard=pedalboard)

    def test_delete_effect_remove_your_connections(self):
        pedalboard = Pedalboard('Pedalboard name')

        builder = Lv2EffectBuilder()
        reverb = builder.build('http://calf.sourceforge.net/plugins/Reverb')
        filter = builder.build('http://calf.sourceforge.net/plugins/Filter')
        reverb2 = builder.build('http://calf.sourceforge.net/plugins/Reverb')

        pedalboard.append(reverb)
        pedalboard.append(filter)
        pedalboard.append(reverb2)

        pedalboard.connect(reverb.outputs[0], filter.inputs[0])
        pedalboard.connect(reverb.outputs[1], filter.inputs[0])
        pedalboard.connect(filter.outputs[0], reverb2.inputs[0])
        pedalboard.connect(reverb.outputs[0], reverb2.inputs[0])

        self.assertEqual(4, len(pedalboard.connections))

        pedalboard.observer = MagicMock()

        pedalboard.effects.remove(filter)

        self.assertEqual(1, len(pedalboard.connections))
        pedalboard.observer.on_connection_updated.assert_not_called()

    def test_data(self):
        pedalboard = Pedalboard('Bank 1')
        pedalboard.observer = MagicMock()

        self.assertEqual({}, pedalboard.data)
        data = {'my-awesome-component': True}
        pedalboard.data = data
        self.assertEqual(data, pedalboard.data)

    def test_index(self):
        bank = Bank('My bank')

        pedalboard1 = Pedalboard(name='My awesome pedalboard')
        pedalboard2 = Pedalboard(name='My awesome pedalboard 2')
        pedalboard3 = Pedalboard(name='My awesome pedalboard 3')

        bank.append(pedalboard1)
        bank.append(pedalboard2)
        bank.append(pedalboard3)

        self.assertEqual(0, pedalboard1.index)
        self.assertEqual(1, pedalboard2.index)
        self.assertEqual(2, pedalboard3.index)

        bank.pedalboards.remove(pedalboard2)

        self.assertEqual(0, pedalboard1.index)
        self.assertEqual(1, pedalboard3.index)

        with self.assertRaises(IndexError):
            pedalboard2.index

    def test_add_system_effect(self):
        pedalboard = Pedalboard('test_add_system_effect')
        with self.assertRaises(NotAddableError):
            pedalboard.append(SystemEffect('System Effect', (), ()))

    def test_update_name(self):
        pedalboard = Pedalboard('Pedalboard 1')
        new_name = 'New name of pedalboard 1'

        pedalboard.observer = MagicMock()
        pedalboard.name = new_name

        self.assertEqual(pedalboard.name, new_name)
        pedalboard.observer.on_custom_change.assert_called_with(CustomChange.PEDALBOARD_NAME, UpdateType.UPDATED, pedalboard=pedalboard)

        # Don't call if is the same name
        pedalboard.observer = MagicMock()
        pedalboard.name = new_name
        pedalboard.observer.on_custom_change.assert_not_called()

    def test_update_data(self):
        pedalboard = Pedalboard('Pedalboard 1')
        pedalboard.observer = MagicMock()

        data = {'level': 50}
        pedalboard.data = data
        pedalboard.observer.on_custom_change.assert_called_with(CustomChange.PEDALBOARD_DATA, UpdateType.UPDATED, pedalboard=pedalboard)

        pedalboard.observer = MagicMock()
        data['level'] = 80
        pedalboard.observer.on_custom_change.assert_not_called()

        pedalboard.data = data
        pedalboard.observer.on_custom_change.assert_called_with(CustomChange.PEDALBOARD_DATA, UpdateType.UPDATED, pedalboard=pedalboard)
