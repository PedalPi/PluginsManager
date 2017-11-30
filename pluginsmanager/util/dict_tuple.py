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


class DictTuple(tuple):
    """
    Dict tuple is a union with dicts and tuples. It's possible obtains an element
    by index or by a key

    The key is not been a int or long instance

    Based in http://jfine-python-classes.readthedocs.io/en/latest/subclass-tuple.html

    :param iterable elements: Elements for the tuple
    :param lambda key_function: Function mapper: it obtains an element and
                                returns your key.
    """

    def __new__(cls, elements, key_function):
        return tuple.__new__(DictTuple, tuple(elements))

    def __init__(self, elements, key_function):
        self._dict = dict(
            (key_function(element), element) for element in elements
        )

    def __getitem__(self, index):
        if isinstance(index, int):
            return super(DictTuple, self).__getitem__(index)

        else:
            return self._dict[index]

    def __contains__(self, item):
        return item in self._dict
