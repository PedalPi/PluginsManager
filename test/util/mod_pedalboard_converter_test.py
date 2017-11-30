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

import os
import unittest
from pathlib import Path
from unittest.mock import MagicMock

from pluginsmanager.model.lv2.lv2_effect_builder import Lv2EffectBuilder
from pluginsmanager.model.system.system_effect import SystemEffect
from pluginsmanager.util.mod_pedalboard_converter import ModPedalboardConverter


class ModPedalboardConverterTest(unittest.TestCase):
    @property
    def mod_converter(self):
        path = Path('/home/paulo/git/mod/mod_ui/')
        #builder = MagicMock()
        builder = Lv2EffectBuilder(ignore_unsupported_plugins=False)
        # builder.reload(builder.lv2_plugins_data())

        return ModPedalboardConverter(path, builder, ignore_errors=True)

    @property
    def here(self):
        return os.path.abspath(os.path.dirname(__file__)) / Path('data')

    @unittest.skipIf('TRAVIS' in os.environ, 'Mod-ui not configured in Travis build')
    def test_all(self):
        converter = self.mod_converter
        pedalboard_path = self.here / Path('teste.pedalboard')

        system_effect = SystemEffect('system', ['capture_1', 'capture_2'], ['playback_1', 'playback_2'])

        print(converter.get_pedalboard_info(pedalboard_path))
        pedalboard = converter.convert(pedalboard_path, system_effect)
        print(pedalboard.json)

    @unittest.skipIf('TRAVIS' in os.environ, 'Mod-ui not configured in Travis build')
    def test_discover_system_effect(self):
        converter = self.mod_converter
        pedalboard_path = self.here / Path('teste.pedalboard')

        print(converter.get_pedalboard_info(pedalboard_path))
        pedalboard = converter.convert(pedalboard_path)
        print(pedalboard.json)

    #@unittest.skipIf('TRAVIS' in os.environ, 'Mod-ui not configured in Travis build')
    @unittest.skip('Raising error: Plugin not installed')
    def test_discover_system_effect_midi(self):
        converter = self.mod_converter
        pedalboard_path = self.here / Path('EPiano.pedalboard')

        print(converter.get_pedalboard_info(pedalboard_path))
        pedalboard = converter.convert(pedalboard_path)
        print(pedalboard.json)

    @unittest.skipIf('TRAVIS' in os.environ, 'Mod-ui not configured in Travis build')
    #@unittest.skip
    def test_discover_system_effect_midi_serial(self):
        converter = self.mod_converter
        pedalboard_path = self.here / Path('EPiano_simple_tt.pedalboard')

        system_effect = SystemEffect(
            'system',
            ['capture_1', 'capture_2'],
            ['playback_1', 'playback_2'],
            ['midi_playback_1'],
            ['midi_capture_1']
        )

        print(converter.get_pedalboard_info(pedalboard_path))
        pedalboard = converter.convert(pedalboard_path)
        print(pedalboard.json)

    @unittest.skipIf('TRAVIS' in os.environ, 'Mod-ui not configured in Travis build')
    #@unittest.skip
    def test_discover_system_effect_midi_serial_2(self):
        converter = self.mod_converter
        pedalboard_path = self.here / Path('setBfree_ttymidi.pedalboard')

        print(converter.get_pedalboard_info(pedalboard_path))
        # Serial midi out raises error
        pedalboard = converter.convert(pedalboard_path)
        print(pedalboard.json)

    @unittest.skipIf('TRAVIS' in os.environ, 'Mod-ui not configured in Travis build')
    # @unittest.skip
    def test_discover_system_effect_i_dont_know(self):
        converter = self.mod_converter
        pedalboard_path = self.here / Path('EPiano_simple.pedalboard')

        print(converter.get_pedalboard_info(pedalboard_path))
        # Serial midi out raises error
        pedalboard = converter.convert(pedalboard_path)
        print(pedalboard.json)

    @unittest.skipIf('TRAVIS' in os.environ, 'Mod-ui not configured in Travis build')
    # @unittest.skip
    def test_discover_system_effect_i_dont_know_2(self):
        converter = self.mod_converter
        pedalboard_path = self.here / Path('setBfree_simple.pedalboard')

        print(converter.get_pedalboard_info(pedalboard_path))
        # Serial midi out raises error
        pedalboard = converter.convert(pedalboard_path)
        print(pedalboard.json)
