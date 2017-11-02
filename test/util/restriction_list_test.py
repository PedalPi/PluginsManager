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
from unittest.mock import MagicMock, call

from pluginsmanager.model.lv2.lv2_effect_builder import Lv2EffectBuilder
from pluginsmanager.observer.update_type import UpdateType
from pluginsmanager.util.restriction_list import RestrictionList


class RestrictionListTest(unittest.TestCase):

    def test_append(self):
        builder = Lv2EffectBuilder()
        element = builder.build('http://calf.sourceforge.net/plugins/Reverb')

        lista = RestrictionList()
        lista.observer = MagicMock()
        lista.append(element)

        lista.observer.assert_called_once_with(UpdateType.CREATED, element, 0)

    def test_insert(self):
        builder = Lv2EffectBuilder()
        element1 = builder.build('http://calf.sourceforge.net/plugins/Reverb')
        element2 = builder.build('http://calf.sourceforge.net/plugins/Reverb')
        element3 = builder.build('http://calf.sourceforge.net/plugins/Reverb')

        lista = RestrictionList()
        lista.append(element1)
        lista.append(element2)

        lista.observer = MagicMock()
        lista.insert(1, element3)

        lista.observer.assert_called_once_with(UpdateType.CREATED, element3, 1)

    def test_remove(self):
        builder = Lv2EffectBuilder()
        element1 = builder.build('http://calf.sourceforge.net/plugins/Reverb')
        element2 = builder.build('http://calf.sourceforge.net/plugins/Reverb')
        element3 = builder.build('http://calf.sourceforge.net/plugins/Reverb')

        lista = RestrictionList()

        lista.append(element1)
        lista.append(element2)
        lista.append(element3)

        lista.observer = MagicMock()
        lista.remove(element2)

        lista.observer.assert_called_once_with(UpdateType.DELETED, element2, 1)

    def test_pop_empty_parameter(self):
        builder = Lv2EffectBuilder()
        a = builder.build('http://calf.sourceforge.net/plugins/Reverb')
        b = builder.build('http://calf.sourceforge.net/plugins/Reverb')
        c = builder.build('http://calf.sourceforge.net/plugins/Reverb')
        d = builder.build('http://calf.sourceforge.net/plugins/Reverb')

        lista = RestrictionList()

        lista.append(a)
        lista.append(b)
        lista.append(c)
        lista.append(d)

        lista.observer = MagicMock()

        self.assertEqual(d, lista.pop())
        self.assertEqual(3, len(lista))

        lista.observer.assert_called_once_with(UpdateType.DELETED, d, len(lista))

    def test_pop_with_parameter(self):
        builder = Lv2EffectBuilder()
        a = builder.build('http://calf.sourceforge.net/plugins/Reverb')
        b = builder.build('http://calf.sourceforge.net/plugins/Reverb')
        c = builder.build('http://calf.sourceforge.net/plugins/Reverb')
        d = builder.build('http://calf.sourceforge.net/plugins/Reverb')

        lista = RestrictionList()

        lista.append(a)
        lista.append(b)
        lista.append(c)
        lista.append(d)

        lista.observer = MagicMock()

        b_index = 1

        self.assertEqual(b, lista.pop(b_index))
        self.assertEqual(3, len(lista))

        lista.observer.assert_called_once_with(UpdateType.DELETED, b, b_index)

    def test__setitem__(self):
        builder = Lv2EffectBuilder()
        a = builder.build('http://calf.sourceforge.net/plugins/Reverb')
        b = builder.build('http://calf.sourceforge.net/plugins/Reverb')
        c = builder.build('http://calf.sourceforge.net/plugins/Reverb')
        d = builder.build('http://calf.sourceforge.net/plugins/Reverb')

        lista = RestrictionList()

        lista.append(a)
        lista.append(b)
        lista.append(c)

        lista.observer = MagicMock()
        index = 1
        old_value = lista[index]
        new_value = d
        lista[index] = new_value

        lista.observer.assert_called_once_with(UpdateType.UPDATED, new_value, index, old=old_value)

    def test__setitem_equal__(self):
        builder = Lv2EffectBuilder()
        a = builder.build('http://calf.sourceforge.net/plugins/Reverb')
        b = builder.build('http://calf.sourceforge.net/plugins/Reverb')
        c = builder.build('http://calf.sourceforge.net/plugins/Reverb')

        lista = RestrictionList()

        lista.append(a)
        lista.append(b)
        lista.append(c)

        lista.observer = MagicMock()
        lista[1] = b

        lista.observer.assert_not_called()

    def test__delitem__(self):
        builder = Lv2EffectBuilder()
        a = builder.build('http://calf.sourceforge.net/plugins/Reverb')
        b = builder.build('http://calf.sourceforge.net/plugins/Reverb')
        c = builder.build('http://calf.sourceforge.net/plugins/Reverb')

        lista = RestrictionList()

        lista.append(a)
        lista.append(b)
        lista.append(c)

        lista.observer = MagicMock()

        index = 1
        del lista[index]

        lista.observer.assert_called_once_with(UpdateType.DELETED, b, index)

    def test_contains(self):
        builder = Lv2EffectBuilder()
        a = builder.build('http://calf.sourceforge.net/plugins/Reverb')
        b = builder.build('http://calf.sourceforge.net/plugins/Reverb')
        c = builder.build('http://calf.sourceforge.net/plugins/Reverb')
        d = builder.build('http://calf.sourceforge.net/plugins/Reverb')

        lista = RestrictionList()

        lista.append(a)
        lista.append(b)
        lista.append(c)

        self.assertTrue(a in lista)
        self.assertTrue(b in lista)
        self.assertTrue(c in lista)

        self.assertFalse(d in lista)
        self.assertTrue(d not in lista)

    def test_swap_not_equals_effects(self):
        builder = Lv2EffectBuilder()
        a = builder.build('http://calf.sourceforge.net/plugins/Reverb')
        b = builder.build('http://calf.sourceforge.net/plugins/Reverb')

        lista = RestrictionList()
        lista.append(a)

        listb = RestrictionList()
        listb.append(b)

        lista.observer = MagicMock()
        listb.observer = MagicMock()

        lista[0], listb[0] = listb[0], lista[0]

        self.assertEqual(b, lista[0])
        self.assertEqual(a, listb[0])

        lista.observer.assert_called_once_with(UpdateType.UPDATED, lista[0], 0, old=listb[0])
        listb.observer.assert_called_once_with(UpdateType.UPDATED, listb[0], 0, old=lista[0])

    def test_move(self):
        builder = Lv2EffectBuilder()
        a = builder.build('http://calf.sourceforge.net/plugins/Reverb')
        b = builder.build('http://calf.sourceforge.net/plugins/Reverb')
        c = builder.build('http://calf.sourceforge.net/plugins/Reverb')
        d = builder.build('http://calf.sourceforge.net/plugins/Reverb')

        lista = RestrictionList()
        lista.append(a)
        lista.append(b)
        lista.append(c)
        lista.append(d)

        lista.observer = MagicMock()

        new_index = 2
        old_index = lista.index(a)
        lista.move(a, new_index)

        self.assertEqual(lista.index(a), new_index)
        self.assertListEqual([b, c, a, d], list(lista))

        expected = [
            call(UpdateType.DELETED, a, old_index),
            call(UpdateType.CREATED, a, new_index)
        ]

        self.assertListEqual(expected, lista.observer.call_args_list)

    def test_move_same_index(self):
        builder = Lv2EffectBuilder()
        a = builder.build('http://calf.sourceforge.net/plugins/Reverb')
        b = builder.build('http://calf.sourceforge.net/plugins/Reverb')
        c = builder.build('http://calf.sourceforge.net/plugins/Reverb')
        d = builder.build('http://calf.sourceforge.net/plugins/Reverb')

        lista = RestrictionList()
        lista.append(a)
        lista.append(b)
        lista.append(c)
        lista.append(d)

        lista.observer = MagicMock()

        same_index = lista.index(a)
        lista.move(a, same_index)

        lista.observer.assert_not_called()
