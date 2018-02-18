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

from pluginsmanager.model.connection import Connection
from pluginsmanager.model.connections_list import ConnectionsList
from pluginsmanager.model.lv2.lv2_effect_builder import Lv2EffectBuilder
from pluginsmanager.model.pedalboard import Pedalboard
from pluginsmanager.util.restriction_list import AlreadyAddedError, NotAddableError


class EffectsListTest(unittest.TestCase):

    def test_append_repeated(self):
        element = MagicMock()

        lista = ConnectionsList(MagicMock())
        lista.append(element)

        with self.assertRaises(AlreadyAddedError):
            lista.append(element)

    def test_append_notaddable(self):
        builder = Lv2EffectBuilder()
        element1 = builder.build('http://calf.sourceforge.net/plugins/Reverb')
        element2 = builder.build('http://calf.sourceforge.net/plugins/Reverb')

        pedalboard = Pedalboard('name')
        connection = Connection(element1.outputs[0], element2.inputs[0])

        with self.assertRaises(NotAddableError):
            pedalboard.connections.append(connection)

        pedalboard.append(element2)

        with self.assertRaises(NotAddableError):
            pedalboard.connections.append(connection)

        pedalboard.append(element1)
        pedalboard.connections.append(connection)  # All effects added - OK

    def test_insert_repeated(self):
        element = MagicMock()

        lista = ConnectionsList(MagicMock())
        lista.insert(1, element)

        with self.assertRaises(AlreadyAddedError):
            lista.insert(1, element)

    def test_remove_not_repeated(self):
        element1 = MagicMock()

        lista = ConnectionsList(MagicMock())

        lista.append(element1)
        lista.remove(element1)
        # Now will raises
        lista.append(element1)

    def test_pop_not_repeated(self):
        element1 = MagicMock()

        lista = ConnectionsList(MagicMock())

        lista.append(element1)
        lista.pop()
        # Now will raises
        lista.append(element1)

    def test__setitem__repeated(self):
        builder = Lv2EffectBuilder()
        element1 = MagicMock()
        element2 = MagicMock()

        lista = ConnectionsList(MagicMock())
        lista.append(element1)
        lista.append(element2)
        lista[0] = element1  # Same effect - Ok

        with self.assertRaises(AlreadyAddedError):
            lista[1] = element1  # Different effect - Error

    def test_del_not_repeated(self):
        element1 = MagicMock()

        lista = ConnectionsList(MagicMock())

        lista.append(element1)
        del lista[0]
        # Now will raises
        lista.append(element1)
