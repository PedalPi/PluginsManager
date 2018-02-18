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

from pluginsmanager.model.effects_list import EffectsList
from pluginsmanager.model.lv2.lv2_effect_builder import Lv2EffectBuilder
from pluginsmanager.model.system.system_effect import SystemEffect
from pluginsmanager.util.restriction_list import AlreadyAddedError, NotAddableError


class EffectsListTest(unittest.TestCase):

    def test_append_repeated(self):
        builder = Lv2EffectBuilder()
        element = builder.build('http://calf.sourceforge.net/plugins/Reverb')

        lista = EffectsList()
        lista.append(element)

        with self.assertRaises(AlreadyAddedError):
            lista.append(element)

    def test_append_notaddable(self):
        lista = EffectsList()
        with self.assertRaises(NotAddableError):
            lista.append(SystemEffect('system', [], []))

    def test_insert_repeated(self):
        builder = Lv2EffectBuilder()
        element = builder.build('http://calf.sourceforge.net/plugins/Reverb')

        lista = EffectsList()
        lista.insert(1, element)

        with self.assertRaises(AlreadyAddedError):
            lista.insert(1, element)

    def test_remove_not_repeated(self):
        builder = Lv2EffectBuilder()
        element1 = builder.build('http://calf.sourceforge.net/plugins/Reverb')

        lista = EffectsList()

        lista.append(element1)
        lista.remove(element1)
        # Now will raises
        lista.append(element1)

    def test_pop_not_repeated(self):
        builder = Lv2EffectBuilder()
        element1 = builder.build('http://calf.sourceforge.net/plugins/Reverb')

        lista = EffectsList()

        lista.append(element1)
        lista.pop()
        # Now will raises
        lista.append(element1)

    def test__setitem__repeated(self):
        builder = Lv2EffectBuilder()
        element1 = builder.build('http://calf.sourceforge.net/plugins/Reverb')
        element2 = builder.build('http://calf.sourceforge.net/plugins/Reverb')

        lista = EffectsList()
        lista.append(element1)
        lista.append(element2)
        lista[0] = element1  # Same effect - Ok

        with self.assertRaises(AlreadyAddedError):
            lista[1] = element1  # Different effect - Error

    def test_del_not_repeated(self):
        builder = Lv2EffectBuilder()
        element1 = builder.build('http://calf.sourceforge.net/plugins/Reverb')

        lista = EffectsList()

        lista.append(element1)
        del lista[0]
        # Now will raises
        lista.append(element1)

    def test_swap(self):
        builder = Lv2EffectBuilder()
        a = builder.build('http://calf.sourceforge.net/plugins/Reverb')
        b = builder.build('http://guitarix.sourceforge.net/plugins/gx_flanger#_flanger')

        lista = EffectsList()
        lista.append(a)
        lista.append(b)

        lista.real_list.observer = MagicMock()

        with self.assertRaises(AlreadyAddedError):
            lista[0], lista[1] = lista[1], lista[0]

        return '''
        self.assertEqual(b, lista[0])
        self.assertEqual(a, lista[1])

        expected = [
            call(UpdateType.UPDATED, lista[0], 0, old=lista[1]),
            call(UpdateType.UPDATED, lista[1], 1, old=lista[0])
        ]

        self.assertListEqual(expected, lista.real_list.observer.call_args_list)
        '''
