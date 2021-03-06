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

from pluginsmanager.observer.observable_list import ObservableList
from pluginsmanager.observer.update_type import UpdateType

from unittest.mock import MagicMock, call


class ObservableListTest(unittest.TestCase):

    def test_append(self):
        element = {'test': 5, 'a':[1,2,3,5]}

        lista = ObservableList()
        lista.observer = MagicMock()
        lista.append(element)

        lista.observer.assert_called_once_with(UpdateType.CREATED, element, 0)

    def test_insert(self):
        lista = ObservableList()
        lista.append(0)
        lista.append(2)

        lista.observer = MagicMock()
        lista.insert(1, 'a')

        lista.observer.assert_called_once_with(UpdateType.CREATED, 'a', 1)

    def test_remove(self):
        lista = ObservableList()

        lista.append(1)
        lista.append('2')
        lista.append(3)

        lista.observer = MagicMock()
        lista.remove('2')

        lista.observer.assert_called_once_with(UpdateType.DELETED, '2', 1)

    def test_pop_empty_parameter(self):
        lista = ObservableList()
        a = 'a'
        b = 'b'
        c = 'c'
        d = 'd'

        lista.append(a)
        lista.append(b)
        lista.append(c)
        lista.append(d)

        lista.observer = MagicMock()

        self.assertEqual(d, lista.pop())
        self.assertEqual(3, len(lista))

        lista.observer.assert_called_once_with(UpdateType.DELETED, d, len(lista))

    def test_pop_with_parameter(self):
        lista = ObservableList()
        a = 'a'
        b = 'b'
        c = 'c'
        d = 'd'

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
        lista = ObservableList()

        lista.append(1)
        lista.append(2)
        lista.append(3)

        lista.observer = MagicMock()
        index = 1
        old_value = lista[index]
        new_value = 4
        lista[index] = new_value

        lista.observer.assert_called_once_with(UpdateType.UPDATED, new_value, index, old=old_value)

    def test__setitem_equal__(self):
        lista = ObservableList()

        lista.append(1)
        lista.append(2)
        lista.append(3)

        lista.observer = MagicMock()
        lista[1] = 2

        lista.observer.assert_not_called()

    def test__delitem__(self):
        lista = ObservableList()

        lista.append(123)
        lista.append(456)
        lista.append(789)

        lista.observer = MagicMock()

        index = 1
        del lista[index]

        lista.observer.assert_called_once_with(UpdateType.DELETED, 456, index)

    def test_contains(self):
        lista = ObservableList()

        lista.append(123)
        lista.append(456)
        lista.append(789)

        self.assertTrue(123 in lista)
        self.assertTrue(456 in lista)
        self.assertTrue(789 in lista)

        self.assertFalse(987 in lista)
        self.assertTrue(987 not in lista)

    def test_swap(self):
        a = {'key': 'value'}
        b = {'key2': 'value2'}

        lista = ObservableList()
        lista.append(a)
        lista.append(b)

        lista.observer = MagicMock()

        lista[0], lista[1] = lista[1], lista[0]
        self.assertEqual(b, lista[0])
        self.assertEqual(a, lista[1])

        expected = [
            call(UpdateType.UPDATED, lista[0], 0, old=lista[1]),
            call(UpdateType.UPDATED, lista[1], 1, old=lista[0])
        ]

        self.assertListEqual(expected, lista.observer.call_args_list)

    def test_swap_2(self):
        a = {'key': 'value'}
        b = {'key2': 'value2'}

        lista = ObservableList()
        lista.append(a)

        listb = ObservableList()
        listb.append(b)

        lista.observer = MagicMock()
        listb.observer = MagicMock()

        lista[0], listb[0] = listb[0], lista[0]

        self.assertEqual(b, lista[0])
        self.assertEqual(a, listb[0])

        lista.observer.assert_called_once_with(UpdateType.UPDATED, lista[0], 0, old=listb[0])
        listb.observer.assert_called_once_with(UpdateType.UPDATED, listb[0], 0, old=lista[0])

    def test_move(self):
        a = {'key': 'value'}
        b = {'key2': 'value2'}
        c = 4
        d = 23

        lista = ObservableList()
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
        a = {'key': 'value'}
        b = {'key2': 'value2'}
        c = 4
        d = 23

        lista = ObservableList()
        lista.append(a)
        lista.append(b)
        lista.append(c)
        lista.append(d)

        lista.observer = MagicMock()

        same_index = lista.index(a)
        lista.move(a, same_index)

        lista.observer.assert_not_called()
