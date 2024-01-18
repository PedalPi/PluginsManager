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

from unittest.mock import MagicMock


class PatchError(Exception):

    def __init__(self, message):
        super(PatchError, self).__init__(message)
        self.message = message


class Patch(metaclass=ABCMeta):
    """
    :class:`.Patch` represents an Audio Plugin Patch::

        >>> my_awesome_effect
        <Lv2Effect object as 'Amp Model' active at 0x7fd58d874ba8>
        >>> my_awesome_effect.patch
        (<Lv2Patch object as value=model.name)

        >>> param.default
        1.5
        >>> param.value = 14

        >>> symbol = param.symbol
        >>> symbol
        'model'
        >>> param == my_awesome_effect.patches[symbol]
        True

    :param Effect effect: Effect in which this parameter belongs
    """

    def __init__(self, effect, uri, default):
        self._uri = uri
        self._effect = effect
        self._default = default
        self._value = default

        self.observer = MagicMock()

    @property
    def effect(self):
        """
        :return: Effect in which this parameter belongs
        """
        return self._effect
    
    @property
    def default(self):
        """
        Parameter default

        :getter: Current default
        :setter: Set the current default
        """
        return self._default
    
    @property
    def uri(self):
        """
        Parameter uri

        :getter: Current uri
        :setter: Set the current uri
        """
        return self._uri
    
    @property
    def value(self):
        """
        Parameter value

        :getter: Current value
        :setter: Set the current value
        """
        return self._value

    @value.setter
    def value(self, new_value):
        if self._value == new_value:
            return
        self._value = new_value
        self.observer.on_patch_value_changed(self)

    def __repr__(self, *args, **kwargs):
        return "<{} object as uri={}, value={} at 0x{:x}>".format(
            self.__class__.__name__,
            self._uri,
            self._value,
            id(self)
        )

    @property
    def json(self):
        """
        Get a json decodable representation of this param

        :return dict: json representation
        """
        return self.__dict__

    @property
    def __dict__(self):
        return {
            'uri': self._uri,
            'value': self._value
        }
