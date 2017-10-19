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

from pluginsmanager.model.connection import ConnectionError
from pluginsmanager.model.lv2.lv2_effect_builder import Lv2EffectBuilder
from pluginsmanager.model.pedalboard import Pedalboard
from pluginsmanager.model.system.system_effect import SystemEffect
from pluginsmanager.observer.update_type import UpdateType


class OutputTest(unittest.TestCase):
    builder = None

    @classmethod
    def setUpClass(cls):
        cls.builder = Lv2EffectBuilder()

    def test_connect(self):
        pedalboard = Pedalboard('Pedalboard name')
        pedalboard.observer = MagicMock()

        builder = OutputTest.builder
        reverb = builder.build('http://calf.sourceforge.net/plugins/Reverb')
        reverb2 = builder.build('http://calf.sourceforge.net/plugins/Reverb')

        pedalboard.append(reverb)
        pedalboard.append(reverb2)

        self.assertEqual(0, len(pedalboard.connections))
        pedalboard.connect(reverb.outputs[0], reverb2.inputs[0])
        self.assertEqual(1, len(pedalboard.connections))

        new_connection = pedalboard.connections[0]
        pedalboard.observer.on_connection_updated.assert_called_with(new_connection, UpdateType.CREATED, pedalboard=pedalboard)

        pedalboard.connect(reverb.outputs[1], reverb2.inputs[1])
        self.assertEqual(2, len(pedalboard.connections))

        new_connection = pedalboard.connections[-1]
        pedalboard.observer.on_connection_updated.assert_called_with(new_connection, UpdateType.CREATED, pedalboard=pedalboard)

    def test_disconnect(self):
        pedalboard = Pedalboard('Pedalboard name')

        builder = OutputTest.builder
        reverb = builder.build('http://calf.sourceforge.net/plugins/Reverb')
        reverb2 = builder.build('http://calf.sourceforge.net/plugins/Reverb')

        pedalboard.append(reverb)
        pedalboard.append(reverb2)

        pedalboard.connect(reverb.outputs[0], reverb2.inputs[0])
        pedalboard.connect(reverb.outputs[1], reverb2.inputs[0])
        self.assertEqual(2, len(pedalboard.connections))

        pedalboard.observer = MagicMock()

        disconnected = pedalboard.connections[-1]
        pedalboard.disconnect(reverb.outputs[1], reverb2.inputs[0])
        self.assertEqual(1, len(pedalboard.connections))
        pedalboard.observer.on_connection_updated.assert_called_with(disconnected, UpdateType.DELETED, pedalboard=pedalboard)

        disconnected = pedalboard.connections[-1]
        pedalboard.disconnect(reverb.outputs[0], reverb2.inputs[0])
        self.assertEqual(0, len(pedalboard.connections))
        pedalboard.observer.on_connection_updated.assert_called_with(disconnected, UpdateType.DELETED, pedalboard=pedalboard)

    def test_disconnect_connection_not_created(self):
        pedalboard = Pedalboard('Pedalboard name')

        builder = OutputTest.builder
        reverb = builder.build('http://calf.sourceforge.net/plugins/Reverb')
        reverb2 = builder.build('http://calf.sourceforge.net/plugins/Reverb')

        pedalboard.append(reverb)
        pedalboard.append(reverb2)

        pedalboard.observer = MagicMock()

        with self.assertRaises(ValueError):
            pedalboard.disconnect(reverb.outputs[1], reverb2.inputs[0])

        pedalboard.observer.on_connection_updated.assert_not_called()

    def test_system_effect_connections(self):
        pedalboard = Pedalboard('A pedalboard')
        sys_effect = SystemEffect('system', ['capture_1'], ['playback_1', 'playback_2'])

        effect_output = sys_effect.outputs[0]
        effect_input = sys_effect.inputs[0]

        pedalboard.connect(effect_output, effect_input)
        self.assertEqual(len(pedalboard.connections), 1)

        pedalboard.disconnect(effect_output, effect_input)
        self.assertEqual(len(pedalboard.connections), 0)
