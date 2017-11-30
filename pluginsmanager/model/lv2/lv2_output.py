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

from pluginsmanager.model.output import Output
from pluginsmanager.model.lv2.lv2_port_mixing import Lv2PortMixing


class Lv2Output(Lv2PortMixing, Output):
    """
    Representation of a Lv2 `output audio port`_ instance.

    For general input use, see :class:`.Output` class documentation.

    .. _output audio port: http://lv2plug.in/ns/lv2core/#OutputPort

    :param Lv2Effect effect: Effect that contains the output
    :param dict data: *output audio port* json representation
    """

    def __init__(self, effect, data):
        super(Lv2Output, self).__init__(effect)
        self._data = data

    @property
    def data(self):
        return self._data
