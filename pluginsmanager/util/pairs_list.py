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
from collections import defaultdict


class PairsList(object):
    """
    Receives two lists and generates a result list of pairs of equal elements

    Uses `calculate` method for generate list

    :param similarity_key_function: Function that receives a element and returns your identifier
                                    to do a mapping with elements from another list
    """

    def __init__(self, similarity_key_function):
        self.similarity_key = similarity_key_function

    def calculate(self, list_a, list_b):
        result = PairsListResult()

        hash_elements_a = self._generate_hash(list_a)
        hash_elements_b = self._generate_hash(list_b)

        keys = hash_elements_a.keys() | hash_elements_b.keys()

        # Pairs
        for key in keys:
            while hash_elements_a[key] and hash_elements_b[key]:
                element_a = hash_elements_a[key].pop(0)
                element_b = hash_elements_b[key].pop(0)

                result.pairs.append((element_a, element_b))

            result.elements_not_added_a.extend(hash_elements_a[key])
            result.elements_not_added_b.extend(hash_elements_b[key])

        return result

    def _generate_hash(self, lista):
        """
        :return: defaultdict(list)
        """
        hash_elements = defaultdict(list)

        for element in lista:
            key = self.similarity_key(element)
            hash_elements[key].append(element)

        return hash_elements


class PairsListResult(object):
    def __init__(self):
        self.pairs = []
        self.elements_not_added_a = []
        self.elements_not_added_b = []
