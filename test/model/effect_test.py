import unittest
from unittest.mock import MagicMock

from pluginsmanager.model.connection import Connection
from pluginsmanager.model.patch import Patch
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
        patch = Patch('Patch name')

        builder = EffectTest.builder
        reverb = builder.build('http://calf.sourceforge.net/plugins/Reverb')
        fuzz = builder.build('http://guitarix.sourceforge.net/plugins/gx_fuzzfacefm_#_fuzzfacefm_')
        reverb2 = builder.build('http://calf.sourceforge.net/plugins/Reverb')

        patch.append(reverb)
        patch.append(fuzz)
        patch.append(reverb2)

        reverb.outputs[0].connect(fuzz.inputs[0])
        reverb.outputs[1].connect(fuzz.inputs[0])
        fuzz.outputs[0].connect(reverb2.inputs[0])
        reverb.outputs[0].connect(reverb2.inputs[0])

        reverb_connections = (
            Connection(reverb.outputs[0], fuzz.inputs[0]),
            Connection(reverb.outputs[1], fuzz.inputs[0]),
            Connection(reverb.outputs[0], reverb2.inputs[0])
        )
        fuzz_connections = (
            Connection(reverb.outputs[0], fuzz.inputs[0]),
            Connection(reverb.outputs[1], fuzz.inputs[0]),
            Connection(fuzz.outputs[0], reverb2.inputs[0])
        )
        reverb2_connections = (
            Connection(fuzz.outputs[0], reverb2.inputs[0]),
            Connection(reverb.outputs[0], reverb2.inputs[0])
        )

        self.assertCountEqual(reverb_connections, reverb.connections)
        self.assertCountEqual(fuzz_connections, fuzz.connections)
        self.assertCountEqual(reverb2_connections, reverb2.connections)
