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

from pluginsmanager.model.lv2.lv2_effect_builder import Lv2EffectBuilder
from pluginsmanager.model.param import ParamError


class ParamTest(unittest.TestCase):
    builder = None

    @classmethod
    def setUpClass(cls):
        cls.builder = Lv2EffectBuilder()

    def test_set_value(self):
        builder = ParamTest.builder
        reverb = builder.build('http://calf.sourceforge.net/plugins/Reverb')

        param = reverb.params[0]
        param.observer = MagicMock()

        param.value = param.minimum
        param.observer.on_param_value_changed.assert_called_with(param)
        param.value = param.maximum
        param.observer.on_param_value_changed.assert_called_with(param)
        param.value = (param.minimum+param.maximum)/2
        param.observer.on_param_value_changed.assert_called_with(param)

        self.assertEqual(3, param.observer.on_param_value_changed.call_count)

    def test_set_equal_value(self):
        builder = ParamTest.builder
        reverb = builder.build('http://calf.sourceforge.net/plugins/Reverb')

        param = reverb.params[0]
        param.observer = MagicMock()

        param.value = param.value

        param.observer.on_param_value_changed.assert_not_called()

    def test_set_invalid_value(self):
        builder = ParamTest.builder
        reverb = builder.build('http://calf.sourceforge.net/plugins/Reverb')

        param = reverb.params[0]
        param.observer = MagicMock()

        with self.assertRaises(ParamError):
            param.value = param.minimum - 1

        with self.assertRaises(ParamError):
            param.value = param.maximum + 1

        param.observer.on_param_value_changed.assert_not_called()

