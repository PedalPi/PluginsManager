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

from abc import ABCMeta, abstractmethod


class Lv2PortMixing(object, metaclass=ABCMeta):
    """
    Contains the default implementation of System ports:
    :class:`.Lv2Input`, :class:`.Lv2Output`,
    :class:`.Lv2MidiInput` and :class:`.Lv2MidiInput`
    """

    def __init__(self, *args, **kwargs):
        super(Lv2PortMixing, self).__init__(*args, **kwargs)
        self._data = None

    @property
    @abstractmethod
    def data(self):
        """
        :return dict: Metadata used for provide the required information
                      in this object
        """
        pass

    def __str__(self):
        return self.data['name']

    @property
    def symbol(self):
        return self.data['symbol']

    @property
    def __dict__(self):
        dictionary = super(Lv2PortMixing, self).__dict__
        dictionary['index'] = self.data['index']

        return dictionary
