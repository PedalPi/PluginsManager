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

from pluginsmanager.util.pairs_list import PairsList


class PairsListTest(unittest.TestCase):

    def test_pairs_list(self):
        similarity_key = lambda element: element

        pairs_list = PairsList(similarity_key)
        list_a = ['A', 'A', 'A', 'B', 'D', 'C', 'X']
        list_b = ['B', 'B', 'D', 'C', 'A', 'A', 'E']

        result = pairs_list.calculate(list_a, list_b)
        expected = [('A', 'A'), ('A', 'A'), ('B', 'B'), ('C', 'C'), ('D', 'D')]

        self.assertEqual(expected, sorted(result.pairs))

        expected_not_pairs_a = ['A', 'X']
        expected_not_pairs_b = ['B', 'E']

        self.assertEqual(expected_not_pairs_a, sorted(result.elements_not_added_a))
        self.assertEqual(expected_not_pairs_b, sorted(result.elements_not_added_b))
