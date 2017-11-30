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

from pluginsmanager.util.dict_tuple import DictTuple


class DictTupleTest(unittest.TestCase):

    def test__get_item__(self):
        elements = ('123', '456', '789')
        data = DictTuple(elements, lambda e: e)

        for index, element in enumerate(elements):
            self.assertEqual(element, data[index])
            self.assertEqual(element, data[element])

    def test_in(self):
        elements = ('abc', 'cde', 'def')
        data = DictTuple(elements, lambda e: e.upper())

        self.assertTrue('ABC' in data)
        self.assertFalse('abc' in data)
