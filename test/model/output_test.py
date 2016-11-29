import unittest

from unittest.mock import MagicMock

from pluginsmanager.model.lv2.lv2_effect_builder import Lv2EffectBuilder
from pluginsmanager.model.pedalboard import Pedalboard

from pluginsmanager.model.update_type import UpdateType


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
        reverb.outputs[0].connect(reverb2.inputs[0])
        self.assertEqual(1, len(pedalboard.connections))

        new_connection = pedalboard.connections[0]
        pedalboard.observer.on_connection_updated.assert_called_with(new_connection, UpdateType.CREATED)

        reverb.outputs[1].connect(reverb2.inputs[1])
        self.assertEqual(2, len(pedalboard.connections))

        new_connection = pedalboard.connections[-1]
        pedalboard.observer.on_connection_updated.assert_called_with(new_connection, UpdateType.CREATED)

    def test_disconnect(self):
        pedalboard = Pedalboard('Pedalboard name')

        builder = OutputTest.builder
        reverb = builder.build('http://calf.sourceforge.net/plugins/Reverb')
        reverb2 = builder.build('http://calf.sourceforge.net/plugins/Reverb')

        pedalboard.append(reverb)
        pedalboard.append(reverb2)

        reverb.outputs[0].connect(reverb2.inputs[0])
        reverb.outputs[1].connect(reverb2.inputs[0])
        self.assertEqual(2, len(pedalboard.connections))

        pedalboard.observer = MagicMock()

        disconnected = pedalboard.connections[-1]
        reverb.outputs[1].disconnect(reverb2.inputs[0])
        self.assertEqual(1, len(pedalboard.connections))
        pedalboard.observer.on_connection_updated.assert_called_with(disconnected, UpdateType.DELETED)

        disconnected = pedalboard.connections[-1]
        reverb.outputs[0].disconnect(reverb2.inputs[0])
        self.assertEqual(0, len(pedalboard.connections))
        pedalboard.observer.on_connection_updated.assert_called_with(disconnected, UpdateType.DELETED)

    def test_disconnect_connection_not_created(self):
        pedalboard = Pedalboard('Pedalboard name')

        builder = OutputTest.builder
        reverb = builder.build('http://calf.sourceforge.net/plugins/Reverb')
        reverb2 = builder.build('http://calf.sourceforge.net/plugins/Reverb')

        pedalboard.append(reverb)
        pedalboard.append(reverb2)

        pedalboard.observer = MagicMock()

        with self.assertRaises(ValueError):
            reverb.outputs[1].disconnect(reverb2.inputs[0])

        pedalboard.observer.on_connection_updated.assert_not_called()
