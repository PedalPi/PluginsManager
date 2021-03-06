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
from pluginsmanager.model.system.system_port_mixing import SystemPortMixing


class SystemOutput(SystemPortMixing, Output):
    """
    Representation of a System output audio port instance.

    For general input use, see :class:`.Output` class documentation.

    :param SystemEffect effect: Effect that contains the input
    :param string symbol: *output audio port* symbol identifier
    """

    def __init__(self, effect, symbol):
        super(SystemOutput, self).__init__(effect)
        self._symbol = symbol

    @property
    def symbol(self):
        return self._symbol
