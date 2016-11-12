import unittest
from unittest.mock import MagicMock

from model.lv2.lv2_effect_builder import Lv2EffectBuilder
from model.param import ParamError


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

