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

from pluginsmanager.model.lv2.lv2_effect_builder import Lv2EffectBuilder
from pluginsmanager.model.system.system_effect import SystemEffect
from pluginsmanager.util.mod_pedalboard_converter import ModPedalboardConverter


class ModPedalboardConverterTest(unittest.TestCase):

    @unittest.skipIf('TRAVIS' in os.environ, 'Mod-ui not configured in Travis build')
    def test_all(self):
        path = Path('/home/paulo/git/mod/mod_ui/')
        builder = Lv2EffectBuilder()
        #builder.reload(builder.lv2_plugins_data())

        converter = ModPedalboardConverter(path, builder)

        pedalboard_path = Path('/home/paulo/.pedalboards/teste.pedalboard')
        system_effect = SystemEffect('system', ['capture_1', 'capture_2'], ['playback_1', 'playback_2'])

        print(converter.get_pedalboard_info(pedalboard_path))
        pedalboard = converter.convert(pedalboard_path, system_effect)
        print(pedalboard.json)
