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

from pluginsmanager.observer.autosaver.index_file import IndexFile
from pluginsmanager.model.bank import Bank


class IndexFileTest(unittest.TestCase):

    def test_load_error(self):
        index = IndexFile(path='/dev/null')
        self.assertListEqual([], index.load([]))

    def test_load_data(self):
        bank1 = Bank(name='Bank 1')
        bank2 = Bank(name='Bank 2')
        bank3 = Bank(name='Bank 3')
        bank4 = Bank(name='Bank 4')

        not_ordered = (bank3, bank2, bank1, bank4)

        # bank1, bank3 Já indexados
        # bank2, bank4 Serão indexados por ordem alfabética
        expected = [bank1, bank3, bank2, bank4]

        index = IndexFile(path='any')

        data = [
            index.generate_index_data(0, bank1),
            index.generate_index_data(1, bank3)
        ]

        result = index.load_data(data, not_ordered)
        self.assertEqual(expected, result)

    def test_generate_data(self):
        bank1 = Bank(name='Bank 1')
        bank2 = Bank(name='Bank 2')
        bank3 = Bank(name='Bank 3')
        bank4 = Bank(name='Bank 4')

        # bank1, bank3 Já indexados
        # bank2, bank4 Serão indexados por ordem alfabética
        banks = [bank1, bank2, bank3, bank4]

        index = IndexFile(path='any')
        result = index.generate_data(banks)

        expected = [
            index.generate_index_data(0, bank1),
            index.generate_index_data(1, bank2),
            index.generate_index_data(2, bank3),
            index.generate_index_data(3, bank4),
        ]

        self.assertEqual(expected, result)
