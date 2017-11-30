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

from pluginsmanager.model.lv2.lv2_effect_builder import Lv2EffectBuilder
from pluginsmanager.model.lv2.lv2_effect_builder import Lv2EffectBuilderError


class Lv2EffecBuilderTest(unittest.TestCase):

    def test_load_nonexistent_effect(self):
        builder = Lv2EffectBuilder()
        with self.assertRaises(Lv2EffectBuilderError):
            builder.build('nonexistent_effect')
