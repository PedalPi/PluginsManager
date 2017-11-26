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

from pluginsmanager.model.param import Param


class Lv2Param(Param):
    """
    Representation of a Lv2 `input control port`_ instance.

    For general input use, see :class:`.Param` class documentation.

    :param Lv2Effect effect: Effect that contains the param
    :param dict data: *input control port* json representation

    .. _input control port: http://lv2plug.in/ns/lv2core/#Parameter
    """

    def __init__(self, effect, data):
        super(Lv2Param, self).__init__(effect, data['ranges']['default'])
        self._data = data

    @property
    def data(self):
        return self._data
    @property
    def maximum(self):
        return self.data['ranges']['maximum']

    @property
    def minimum(self):
        return self.data['ranges']['minimum']

    @property
    def symbol(self):
        return self.data['symbol']

    @property
    def __dict__(self):
        dictionary = super(Lv2Param, self).__dict__
        dictionary['index'] = self.data['index']

        return dictionary
