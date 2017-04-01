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

from pluginsmanager.model.input import Input


class SystemInput(Input):

    def __init__(self, effect, system_input):
        super(SystemInput, self).__init__(effect)
        self._input = system_input
        self._unique_for_all_pedalboards = True

    def __str__(self):
        return self._input

    def __repr__(self):
        return "<{} object as {} at 0x{:x}>".format(
            self.__class__.__name__,
            str(self),
            id(self)
        )

    @property
    def symbol(self):
        return str(self)

    @property
    def __dict__(self):
        return {
            'symbol': self.symbol,
            'index': self.effect.inputs.index(self),
        }
