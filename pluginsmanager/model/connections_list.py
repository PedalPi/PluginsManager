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

from pluginsmanager.util.restriction_list import RestrictionList, AlreadyAddedError, NotAddableError


class ConnectionsList(RestrictionList):
    """
    ConnectionsList contains a :class:`.ObservableList`
    and checks the effect instance unity restrictions
    """

    def __init__(self, pedalboard):
        super(ConnectionsList, self).__init__()
        self.pedalboard = pedalboard

    def check_insertion(self, item):
        if item in self._items:
            raise AlreadyAddedError("The connection '{}' already added".format(item))

        input_effect = item.input.effect
        output_effect = item.output.effect

        if not input_effect.is_unique_for_all_pedalboards\
        and input_effect not in self.pedalboard.effects:
            raise NotAddableError(
                "The effect '{}' of input port '{}' hasn't added in the pedalboard. "
                "Please, append it first.".format(input_effect, item.input))

        if not output_effect.is_unique_for_all_pedalboards\
        and output_effect not in self.pedalboard.effects:
            raise NotAddableError(
                "The effect '{}' of output port '{}' hasn't added in the pedalboard. "
                "Please, append it first.".format(output_effect, item.output))
