import unittest

from unittest.mock import MagicMock

from model.lv2.lv2_effect_builder import Lv2EffectBuilder
from model.patch import Patch

from model.update_type import UpdateType


class OutputTest(unittest.TestCase):
    builder = None

    @classmethod
    def setUpClass(cls):
        cls.builder = Lv2EffectBuilder()

    def test_connect(self):
        patch = Patch('Patch name')
        patch.observer = MagicMock()

        builder = OutputTest.builder
        reverb = builder.build('http://calf.sourceforge.net/plugins/Reverb')
        reverb2 = builder.build('http://calf.sourceforge.net/plugins/Reverb')

        patch.append(reverb)
        patch.append(reverb2)

        self.assertEqual(0, len(patch.connections))
        reverb.outputs[0].connect(reverb2.inputs[0])
        self.assertEqual(1, len(patch.connections))

        new_connection = patch.connections[0]
        patch.observer.on_connection_updated.assert_called_with(new_connection, UpdateType.CREATED)

        reverb.outputs[1].connect(reverb2.inputs[1])
        self.assertEqual(2, len(patch.connections))

        new_connection = patch.connections[-1]
        patch.observer.on_connection_updated.assert_called_with(new_connection, UpdateType.CREATED)

    def test_disconnect(self):
        patch = Patch('Patch name')

        builder = OutputTest.builder
        reverb = builder.build('http://calf.sourceforge.net/plugins/Reverb')
        reverb2 = builder.build('http://calf.sourceforge.net/plugins/Reverb')

        patch.append(reverb)
        patch.append(reverb2)

        reverb.outputs[0].connect(reverb2.inputs[0])
        reverb.outputs[1].connect(reverb2.inputs[0])
        self.assertEqual(2, len(patch.connections))

        patch.observer = MagicMock()

        disconnected = patch.connections[-1]
        reverb.outputs[1].disconnect(reverb2.inputs[0])
        self.assertEqual(1, len(patch.connections))
        patch.observer.on_connection_updated.assert_called_with(disconnected, UpdateType.DELETED)

        disconnected = patch.connections[-1]
        reverb.outputs[0].disconnect(reverb2.inputs[0])
        self.assertEqual(0, len(patch.connections))
        patch.observer.on_connection_updated.assert_called_with(disconnected, UpdateType.DELETED)

    def test_disconnect_connection_not_created(self):
        patch = Patch('Patch name')

        builder = OutputTest.builder
        reverb = builder.build('http://calf.sourceforge.net/plugins/Reverb')
        reverb2 = builder.build('http://calf.sourceforge.net/plugins/Reverb')

        patch.append(reverb)
        patch.append(reverb2)

        patch.observer = MagicMock()

        with self.assertRaises(ValueError):
            reverb.outputs[1].disconnect(reverb2.inputs[0])

        patch.observer.on_connection_updated.assert_not_called()
