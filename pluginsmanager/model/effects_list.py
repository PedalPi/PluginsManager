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


class EffectsList(RestrictionList):
    """
    EffectsList contains a :class:`.ObservableList`
    and checks the effect instance unity restrictions
    """

    def check_insertion(self, item):
        if item in self._items:
            raise AlreadyAddedError("The effect '{}' already added".format(item))

        if item.is_unique_for_all_pedalboards:
            raise NotAddableError(
                "The effect '{}' can't added in this list because "
                "isn't allowed add it in any pedalboard".format(item))
