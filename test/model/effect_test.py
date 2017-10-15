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

from pluginsmanager.model.connection import Connection
from pluginsmanager.model.pedalboard import Pedalboard
from pluginsmanager.model.lv2.lv2_effect_builder import Lv2EffectBuilder


class EffectTest(unittest.TestCase):
    builder = None

    @classmethod
    def setUpClass(cls):
        cls.builder = Lv2EffectBuilder()

    def test_active(self):
        builder = EffectTest.builder
        reverb = builder.build('http://calf.sourceforge.net/plugins/Reverb')

        reverb.observer = MagicMock()

        self.assertEqual(True, reverb.active)
        reverb.active = False
        reverb.observer.on_effect_status_toggled.assert_called_with(reverb)
        self.assertEqual(False, reverb.active)

    def test_active_same_state(self):
        builder = EffectTest.builder
        reverb = builder.build('http://calf.sourceforge.net/plugins/Reverb')

        reverb.observer = MagicMock()

        self.assertEqual(True, reverb.active)
        reverb.active = True
        reverb.observer.on_effect_status_toggled.assert_not_called()

    def test_toggle(self):
        builder = EffectTest.builder
        reverb = builder.build('http://calf.sourceforge.net/plugins/Reverb')

        reverb.observer = MagicMock()

        self.assertEqual(True, reverb.active)
        reverb.toggle()
        reverb.observer.on_effect_status_toggled.assert_called_with(reverb)
        self.assertEqual(False, reverb.active)

    def test_connections_effect_remove_your_connections(self):
        pedalboard = Pedalboard('Pedalboard name')

        builder = EffectTest.builder
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

        reverb_connections = (
            Connection(reverb.outputs[0], filter.inputs[0]),
            Connection(reverb.outputs[1], filter.inputs[0]),
            Connection(reverb.outputs[0], reverb2.inputs[0])
        )
        fuzz_connections = (
            Connection(reverb.outputs[0], filter.inputs[0]),
            Connection(reverb.outputs[1], filter.inputs[0]),
            Connection(filter.outputs[0], reverb2.inputs[0])
        )
        reverb2_connections = (
            Connection(filter.outputs[0], reverb2.inputs[0]),
            Connection(reverb.outputs[0], reverb2.inputs[0])
        )

        self.assertCountEqual(reverb_connections, reverb.connections)
        self.assertCountEqual(fuzz_connections, filter.connections)
        self.assertCountEqual(reverb2_connections, reverb2.connections)

    def test_index(self):
        builder = EffectTest.builder
        reverb1 = builder.build('http://calf.sourceforge.net/plugins/Reverb')
        reverb2 = builder.build('http://calf.sourceforge.net/plugins/Reverb')
        reverb3 = builder.build('http://calf.sourceforge.net/plugins/Reverb')

        pedalboard = Pedalboard(name='My awesome pedalboard')
        pedalboard.append(reverb1)
        pedalboard.append(reverb2)
        pedalboard.append(reverb3)

        self.assertEqual(0, reverb1.index)
        self.assertEqual(1, reverb2.index)
        self.assertEqual(2, reverb3.index)

        pedalboard.effects.remove(reverb2)

        self.assertEqual(0, reverb1.index)
        self.assertEqual(1, reverb3.index)

        with self.assertRaises(IndexError):
            reverb2.index
