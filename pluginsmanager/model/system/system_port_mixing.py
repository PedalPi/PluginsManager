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

from abc import ABCMeta


class SystemPortMixing(object, metaclass=ABCMeta):
    """
    Contains the default implementation of System ports:
    :class:`.SystemInput`, :class:`.SystemOutput`,
    :class:`.SystemMidiInput` and :class:`.SystemMidiInput`

    If you uses it, in the class constructor is necessary
    define the symbol (`string`)::

        class MySystemPort(SystemPortMixing, InputPort):
            def __init__(self, effect):
                super(MySystemPort, self).__init__(effect)
                self._symbol = 'symbol'
    """

    def __init__(self, *args, **kwargs):
        super(SystemPortMixing, self).__init__(*args, **kwargs)
        self._symbol = None

    def __str__(self):
        return self._symbol

    @property
    def __dict__(self):
        return {
            'symbol': self.symbol,
            'index': self.index(),
        }
