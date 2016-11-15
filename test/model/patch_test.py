import unittest
from unittest.mock import MagicMock

from pluginsmanager.model.patch import Patch
from pluginsmanager.model.update_type import UpdateType

from pluginsmanager.model.lv2.lv2_effect_builder import Lv2EffectBuilder


class PatchTest(unittest.TestCase):

    def test_add_effect_by_effects(self):
        patch = Patch('Patch 1')

        effect1 = MagicMock()
        effect2 = MagicMock()

        patch.observer = MagicMock()

        patch.effects.append(effect1)
        self.assertEqual(effect1.patch, patch)
        self.assertEqual(patch.effects[0], effect1)
        patch.observer.on_effect_updated.assert_called_with(effect1, UpdateType.CREATED)

        patch.effects.append(effect2)
        self.assertEqual(effect2.patch, patch)
        self.assertEqual(patch.effects[1], effect2)
        patch.observer.on_effect_updated.assert_called_with(effect2, UpdateType.CREATED)

    def test_add_effect(self):
        patch = Patch('Patch 1')

        effect1 = MagicMock()
        effect2 = MagicMock()

        patch.observer = MagicMock()

        patch.append(effect1)
        self.assertEqual(effect1.patch, patch)
        self.assertEqual(patch.effects[0], effect1)
        patch.observer.on_effect_updated.assert_called_with(effect1, UpdateType.CREATED)

        patch.append(effect2)
        self.assertEqual(effect2.patch, patch)
        self.assertEqual(patch.effects[1], effect2)
        patch.observer.on_effect_updated.assert_called_with(effect2, UpdateType.CREATED)

    def test_update_effect(self):
        patch = Patch('Patch 1')

        effect1 = MagicMock()
        effect2 = MagicMock()

        patch.append(effect1)

        patch.observer = MagicMock()
        patch.effects[0] = effect2

        self.assertEqual(effect2.patch, patch)
        self.assertEqual(patch.effects[0], effect2)
        patch.observer.on_effect_updated.assert_called_with(effect2, UpdateType.UPDATED)

    def test_delete_effect(self):
        patch = Patch('Bank 1')

        effect = MagicMock()

        patch.append(effect)

        patch.observer = MagicMock()
        del patch.effects[0]

        self.assertEqual(effect.patch, None)
        self.assertEqual(len(patch.effects), 0)
        patch.observer.on_effect_updated.assert_called_with(effect, UpdateType.DELETED)

    def test_add_connection_by_connections(self):
        """ Other mode is by output.connect(input)"""
        patch = Patch('Patch 1')

        connection1 = MagicMock()
        connection2 = MagicMock()

        patch.observer = MagicMock()

        patch.connections.append(connection1)
        self.assertEqual(patch.connections[0], connection1)
        patch.observer.on_connection_updated.assert_called_with(connection1, UpdateType.CREATED)

        patch.connections.append(connection2)
        self.assertEqual(patch.connections[1], connection2)
        patch.observer.on_connection_updated.assert_called_with(connection2, UpdateType.CREATED)

    def test_update_connection(self):
        patch = Patch('Patch 1')

        connection1 = MagicMock()
        connection2 = MagicMock()

        patch.connections.append(connection1)

        patch.observer = MagicMock()
        patch.connections[0] = connection2

        self.assertEqual(patch.connections[0], connection2)
        patch.observer.on_connection_updated.assert_called_with(connection2, UpdateType.UPDATED)

    def test_delete_connection(self):
        """ Other mode is by output.disconnect(input)"""
        patch = Patch('Bank 1')

        connection = MagicMock()

        patch.connections.append(connection)

        patch.observer = MagicMock()
        del patch.connections[0]

        self.assertEqual(len(patch.connections), 0)
        patch.observer.on_connection_updated.assert_called_with(connection, UpdateType.DELETED)

    def test_delete_effect_remove_your_connections(self):
        patch = Patch('Patch name')

        builder = Lv2EffectBuilder()
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

        self.assertEqual(4, len(patch.connections))

        patch.observer = MagicMock()
        fuzz_connections = fuzz.connections

        patch.effects.remove(fuzz)

        self.assertEqual(1, len(patch.connections))
        for connection in fuzz_connections:
            patch.observer.on_connection_updated.assert_any_call(connection, UpdateType.DELETED)
