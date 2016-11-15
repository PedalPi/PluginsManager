import unittest
from unittest.mock import MagicMock

from pluginsmanager.model.bank import Bank
from pluginsmanager.model.update_type import UpdateType

from pluginsmanager.model.patch import Patch
from pluginsmanager.model.lv2.lv2_effect_builder import Lv2EffectBuilder

import json


class BankTest(unittest.TestCase):

    def test_add_patch_by_patches(self):
        bank = Bank('Bank 1')

        patch1 = MagicMock()
        patch2 = MagicMock()

        bank.observer = MagicMock()

        bank.patches.append(patch1)
        self.assertEqual(patch1.bank, bank)
        self.assertEqual(bank.patches[0], patch1)
        bank.observer.on_patch_updated.assert_called_with(patch1, UpdateType.CREATED)

        bank.patches.append(patch2)
        self.assertEqual(patch2.bank, bank)
        self.assertEqual(bank.patches[1], patch2)
        bank.observer.on_patch_updated.assert_called_with(patch2, UpdateType.CREATED)

    def test_add_patch(self):
        bank = Bank('Bank 1')

        patch1 = MagicMock()
        patch2 = MagicMock()

        bank.observer = MagicMock()

        bank.append(patch1)
        self.assertEqual(patch1.bank, bank)
        self.assertEqual(bank.patches[0], patch1)
        bank.observer.on_patch_updated.assert_called_with(patch1, UpdateType.CREATED)

        bank.append(patch2)
        self.assertEqual(patch2.bank, bank)
        self.assertEqual(bank.patches[1], patch2)
        bank.observer.on_patch_updated.assert_called_with(patch2, UpdateType.CREATED)

    def test_update_patch(self):
        bank = Bank('Bank 1')

        patch1 = MagicMock()
        patch2 = MagicMock()

        bank.append(patch1)

        bank.observer = MagicMock()
        bank.patches[0] = patch2

        self.assertEqual(patch2.bank, bank)
        self.assertEqual(bank.patches[0], patch2)
        bank.observer.on_patch_updated.assert_called_with(patch2, UpdateType.UPDATED)

    def test_delete_patch(self):
        bank = Bank('Bank 1')

        patch = MagicMock()

        bank.append(patch)

        bank.observer = MagicMock()
        del bank.patches[0]

        self.assertEqual(patch.bank, None)
        self.assertEqual(len(bank.patches), 0)
        bank.observer.on_patch_updated.assert_called_with(patch, UpdateType.DELETED)

    def test_json(self):


        bank = Bank('Bank 1')
        patch = Patch('Rocksmith')

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

        bank.append(patch)

        print(json.dumps(bank.json, sort_keys=True, indent=2))
