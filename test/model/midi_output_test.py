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


class MidiOutputTest(unittest.TestCase):
    builder = None

    @classmethod
    def setUpClass(cls):
        cls.builder = Lv2EffectBuilder()

    def test_connect(self):
        pedalboard = Pedalboard('Pedalboard name')
        pedalboard.observer = MagicMock()

        builder = MidiOutputTest.builder
        cctonode = builder.build('http://gareus.org/oss/lv2/midifilter#cctonote')
        cctonode2 = builder.build('http://gareus.org/oss/lv2/midifilter#cctonote')

        pedalboard.append(cctonode)
        pedalboard.append(cctonode2)

        self.assertEqual(0, len(pedalboard.connections))
        pedalboard.connect(cctonode.midi_outputs[0], cctonode2.midi_inputs[0])
        self.assertEqual(1, len(pedalboard.connections))

        new_connection = pedalboard.connections[0]
        pedalboard.observer.on_connection_updated.assert_called_with(new_connection, UpdateType.CREATED, pedalboard=pedalboard)

        pedalboard.connect(cctonode.midi_outputs[0], cctonode2.midi_inputs[0])
        self.assertEqual(2, len(pedalboard.connections))

        new_connection = pedalboard.connections[-1]
        pedalboard.observer.on_connection_updated.assert_called_with(new_connection, UpdateType.CREATED, pedalboard=pedalboard)

    def test_disconnect(self):
        pedalboard = Pedalboard('Pedalboard name')

        builder = MidiOutputTest.builder
        cctonode = builder.build('http://gareus.org/oss/lv2/midifilter#cctonote')
        cctonode2 = builder.build('http://gareus.org/oss/lv2/midifilter#cctonote')

        pedalboard.append(cctonode)
        pedalboard.append(cctonode2)

        pedalboard.connect(cctonode.midi_outputs[0], cctonode2.midi_inputs[0])
        self.assertEqual(1, len(pedalboard.connections))

        pedalboard.observer = MagicMock()

        disconnected = pedalboard.connections[-1]
        pedalboard.disconnect(cctonode.midi_outputs[0], cctonode2.midi_inputs[0])
        self.assertEqual(0, len(pedalboard.connections))
        pedalboard.observer.on_connection_updated.assert_called_with(disconnected, UpdateType.DELETED, pedalboard=pedalboard)

    def test_disconnect_connection_not_created(self):
        pedalboard = Pedalboard('Pedalboard name')

        builder = MidiOutputTest.builder
        cctonode = builder.build('http://gareus.org/oss/lv2/midifilter#cctonote')
        cctonode2 = builder.build('http://gareus.org/oss/lv2/midifilter#cctonote')

        pedalboard.append(cctonode)
        pedalboard.append(cctonode2)

        pedalboard.observer = MagicMock()

        with self.assertRaises(ValueError):
            pedalboard.disconnect(cctonode.midi_outputs[0], cctonode2.midi_inputs[0])

        pedalboard.observer.on_connection_updated.assert_not_called()

    def test_system_effect_connections(self):
        pedalboard = Pedalboard('A pedalboard')
        sys_effect = SystemEffect(
            'system',
            ['capture_1'],
            ['playback_1', 'playback_2'],
            ['midi_capture_1'],
            ['midi_playback_1']
        )

        effect_output = sys_effect.midi_outputs[0]
        effect_input = sys_effect.midi_inputs[0]

        pedalboard.connect(effect_output, effect_input)
        self.assertEqual(len(pedalboard.connections), 1)

        pedalboard.disconnect(effect_output, effect_input)
        self.assertEqual(len(pedalboard.connections), 0)

    def test_port_symbol(self):
        builder = MidiOutputTest.builder
        cctonode = builder.build('http://gareus.org/oss/lv2/midifilter#cctonote')
        sys_effect = SystemEffect(
            'system',
            ['capture_1'],
            ['playback_1', 'playback_2'],
            ['midi_capture_1'],
            ['midi_playback_1']
        )

        self.port_symbol_test(cctonode)
        self.port_symbol_test(sys_effect)

    def port_symbol_test(self, effect):
        port = effect.midi_outputs[0]
        self.assertEqual(effect.midi_outputs[port.index], effect.midi_outputs[port.symbol])
        port = effect.midi_inputs[0]
        self.assertEqual(effect.midi_inputs[port.index], effect.midi_inputs[port.symbol])
