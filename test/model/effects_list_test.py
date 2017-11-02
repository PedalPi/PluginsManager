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

from pluginsmanager.model.system.system_effect import SystemEffect
from pluginsmanager.model.effects_list import EffectsList, AlreadyAddedError, NotAddableError
from pluginsmanager.model.lv2.lv2_effect_builder import Lv2EffectBuilder
from pluginsmanager.observer.update_type import UpdateType


class EffectsListTest(unittest.TestCase):

    def test_append(self):
        builder = Lv2EffectBuilder()
        element = builder.build('http://calf.sourceforge.net/plugins/Reverb')

        lista = EffectsList()
        lista.real_list.observer = MagicMock()
        lista.append(element)

        lista.real_list.observer.assert_called_once_with(UpdateType.CREATED, element, 0)

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

    def test_insert(self):
        builder = Lv2EffectBuilder()
        element1 = builder.build('http://calf.sourceforge.net/plugins/Reverb')
        element2 = builder.build('http://calf.sourceforge.net/plugins/Reverb')
        element3 = builder.build('http://calf.sourceforge.net/plugins/Reverb')

        lista = EffectsList()
        lista.append(element1)
        lista.append(element2)

        lista.real_list.observer = MagicMock()
        lista.insert(1, element3)

        lista.real_list.observer.assert_called_once_with(UpdateType.CREATED, element3, 1)

    def test_insert_repeated(self):
        builder = Lv2EffectBuilder()
        element = builder.build('http://calf.sourceforge.net/plugins/Reverb')

        lista = EffectsList()
        lista.insert(1, element)

        with self.assertRaises(AlreadyAddedError):
            lista.insert(1, element)

    def test_remove(self):
        builder = Lv2EffectBuilder()
        element1 = builder.build('http://calf.sourceforge.net/plugins/Reverb')
        element2 = builder.build('http://calf.sourceforge.net/plugins/Reverb')
        element3 = builder.build('http://calf.sourceforge.net/plugins/Reverb')

        lista = EffectsList()

        lista.append(element1)
        lista.append(element2)
        lista.append(element3)

        lista.real_list.observer = MagicMock()
        lista.remove(element2)

        lista.real_list.observer.assert_called_once_with(UpdateType.DELETED, element2, 1)

    def test_remove_not_repeated(self):
        builder = Lv2EffectBuilder()
        element1 = builder.build('http://calf.sourceforge.net/plugins/Reverb')

        lista = EffectsList()

        lista.append(element1)
        lista.remove(element1)
        # Now will raises
        lista.append(element1)

    def test_pop_empty_parameter(self):
        builder = Lv2EffectBuilder()
        a = builder.build('http://calf.sourceforge.net/plugins/Reverb')
        b = builder.build('http://calf.sourceforge.net/plugins/Reverb')
        c = builder.build('http://calf.sourceforge.net/plugins/Reverb')
        d = builder.build('http://calf.sourceforge.net/plugins/Reverb')

        lista = EffectsList()

        lista.append(a)
        lista.append(b)
        lista.append(c)
        lista.append(d)

        lista.real_list.observer = MagicMock()

        self.assertEqual(d, lista.pop())
        self.assertEqual(3, len(lista))

        lista.real_list.observer.assert_called_once_with(UpdateType.DELETED, d, len(lista))

    def test_pop_with_parameter(self):
        builder = Lv2EffectBuilder()
        a = builder.build('http://calf.sourceforge.net/plugins/Reverb')
        b = builder.build('http://calf.sourceforge.net/plugins/Reverb')
        c = builder.build('http://calf.sourceforge.net/plugins/Reverb')
        d = builder.build('http://calf.sourceforge.net/plugins/Reverb')

        lista = EffectsList()

        lista.append(a)
        lista.append(b)
        lista.append(c)
        lista.append(d)

        lista.real_list.observer = MagicMock()

        b_index = 1

        self.assertEqual(b, lista.pop(b_index))
        self.assertEqual(3, len(lista))

        lista.real_list.observer.assert_called_once_with(UpdateType.DELETED, b, b_index)

    def test_pop_not_repeated(self):
        builder = Lv2EffectBuilder()
        element1 = builder.build('http://calf.sourceforge.net/plugins/Reverb')

        lista = EffectsList()

        lista.append(element1)
        lista.pop()
        # Now will raises
        lista.append(element1)

    def test__setitem__(self):
        builder = Lv2EffectBuilder()
        a = builder.build('http://calf.sourceforge.net/plugins/Reverb')
        b = builder.build('http://calf.sourceforge.net/plugins/Reverb')
        c = builder.build('http://calf.sourceforge.net/plugins/Reverb')
        d = builder.build('http://calf.sourceforge.net/plugins/Reverb')

        lista = EffectsList()

        lista.append(a)
        lista.append(b)
        lista.append(c)

        lista.real_list.observer = MagicMock()
        index = 1
        old_value = lista[index]
        new_value = d
        lista[index] = new_value

        lista.real_list.observer.assert_called_once_with(UpdateType.UPDATED, new_value, index, old=old_value)

    def test__setitem_equal__(self):
        builder = Lv2EffectBuilder()
        a = builder.build('http://calf.sourceforge.net/plugins/Reverb')
        b = builder.build('http://calf.sourceforge.net/plugins/Reverb')
        c = builder.build('http://calf.sourceforge.net/plugins/Reverb')

        lista = EffectsList()

        lista.append(a)
        lista.append(b)
        lista.append(c)

        lista.real_list.observer = MagicMock()
        lista[1] = b

        lista.real_list.observer.assert_not_called()

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

    def test__delitem__(self):
        builder = Lv2EffectBuilder()
        a = builder.build('http://calf.sourceforge.net/plugins/Reverb')
        b = builder.build('http://calf.sourceforge.net/plugins/Reverb')
        c = builder.build('http://calf.sourceforge.net/plugins/Reverb')

        lista = EffectsList()

        lista.append(a)
        lista.append(b)
        lista.append(c)

        lista.real_list.observer = MagicMock()

        index = 1
        del lista[index]

        lista.real_list.observer.assert_called_once_with(UpdateType.DELETED, b, index)

    def test_del_not_repeated(self):
        builder = Lv2EffectBuilder()
        element1 = builder.build('http://calf.sourceforge.net/plugins/Reverb')

        lista = EffectsList()

        lista.append(element1)
        del lista[0]
        # Now will raises
        lista.append(element1)

    def test_contains(self):
        builder = Lv2EffectBuilder()
        a = builder.build('http://calf.sourceforge.net/plugins/Reverb')
        b = builder.build('http://calf.sourceforge.net/plugins/Reverb')
        c = builder.build('http://calf.sourceforge.net/plugins/Reverb')
        d = builder.build('http://calf.sourceforge.net/plugins/Reverb')

        lista = EffectsList()

        lista.append(a)
        lista.append(b)
        lista.append(c)

        self.assertTrue(a in lista)
        self.assertTrue(b in lista)
        self.assertTrue(c in lista)

        self.assertFalse(d in lista)
        self.assertTrue(d not in lista)

    def test_swap(self):
        builder = Lv2EffectBuilder()
        a = builder.build('http://calf.sourceforge.net/plugins/Reverb')
        b = builder.build('http://guitarix.sourceforge.net/plugins/gx_fuzzfacefm_#_fuzzfacefm_')

        lista = EffectsList()
        lista.append(a)
        lista.append(b)

        lista.real_list.observer = MagicMock()

        with self.assertRaises(AlreadyAddedError):
            lista[0], lista[1] = lista[1], lista[0]

        old_code = '''
        self.assertEqual(b, lista[0])
        self.assertEqual(a, lista[1])

        expected = [
            call(UpdateType.UPDATED, lista[0], 0, old=lista[1]),
            call(UpdateType.UPDATED, lista[1], 1, old=lista[0])
        ]

        self.assertListEqual(expected, lista.real_list.observer.call_args_list)
        '''
        return

    def test_swap_2(self):
        builder = Lv2EffectBuilder()
        a = builder.build('http://calf.sourceforge.net/plugins/Reverb')
        b = builder.build('http://calf.sourceforge.net/plugins/Reverb')

        lista = EffectsList()
        lista.append(a)

        listb = EffectsList()
        listb.append(b)

        lista.real_list.observer = MagicMock()
        listb.real_list.observer = MagicMock()

        lista[0], listb[0] = listb[0], lista[0]

        self.assertEqual(b, lista[0])
        self.assertEqual(a, listb[0])

        lista.real_list.observer.assert_called_once_with(UpdateType.UPDATED, lista[0], 0, old=listb[0])
        listb.real_list.observer.assert_called_once_with(UpdateType.UPDATED, listb[0], 0, old=lista[0])

    def test_move(self):
        builder = Lv2EffectBuilder()
        a = builder.build('http://calf.sourceforge.net/plugins/Reverb')
        b = builder.build('http://calf.sourceforge.net/plugins/Reverb')
        c = builder.build('http://calf.sourceforge.net/plugins/Reverb')
        d = builder.build('http://calf.sourceforge.net/plugins/Reverb')

        lista = EffectsList()
        lista.append(a)
        lista.append(b)
        lista.append(c)
        lista.append(d)

        lista.real_list.observer = MagicMock()

        new_index = 2
        old_index = lista.index(a)
        lista.move(a, new_index)

        self.assertEqual(lista.index(a), new_index)
        self.assertListEqual([b, c, a, d], list(lista))

        expected = [
            call(UpdateType.DELETED, a, old_index),
            call(UpdateType.CREATED, a, new_index)
        ]

        self.assertListEqual(expected, lista.real_list.observer.call_args_list)

    def test_move_same_index(self):
        builder = Lv2EffectBuilder()
        a = builder.build('http://calf.sourceforge.net/plugins/Reverb')
        b = builder.build('http://calf.sourceforge.net/plugins/Reverb')
        c = builder.build('http://calf.sourceforge.net/plugins/Reverb')
        d = builder.build('http://calf.sourceforge.net/plugins/Reverb')

        lista = EffectsList()
        lista.append(a)
        lista.append(b)
        lista.append(c)
        lista.append(d)

        lista.real_list.observer = MagicMock()

        same_index = lista.index(a)
        lista.move(a, same_index)

        lista.real_list.observer.assert_not_called()
