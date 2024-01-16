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

from pluginsmanager.model.patch import Patch


class Lv2Patch(Patch):
    """
    Representation of a Lv2 patch.

    For general input use, see :class:`.Patch` class documentation.

    :param Lv2Effect effect: Effect that contains the patchy
    :param str symbol: symbol for the effect

    .. _patch: http://lv2plug.in/ns/ext/patch#
    """

    def __init__(self, effect, uri, default):
        super(Lv2Patch, self).__init__(effect, default)
        self._uri = uri
        self._name = uri.rsplit('#', 1)[-1]

    @property
    def name(self):
        return self._name

    @property
    def uri(self):
        return self._uri

    @property
    def __dict__(self):
        dictionary = super(Lv2Patch, self).__dict__
        return dictionary
