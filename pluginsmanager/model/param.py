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


class ParamError(Exception):

    def __init__(self, message):
        super(ParamError, self).__init__(message)
        self.message = message


class Param(metaclass=ABCMeta):
    """
    :class:`.Param` represents an Audio Plugin Parameter::

        >>> my_awesome_effect
        <Lv2Effect object as 'Calf Reverb' active at 0x7fd58d874ba8>
        >>> my_awesome_effect.params
        (<Lv2Param object as value=1.5 [0.4000000059604645 - 15.0] at 0x7fd587f77908>, <Lv2Param object as value=5000.0 [2000.0 - 20000.0] at 0x7fd587f7a9e8>, <Lv2Param object as value=2 [0 - 5] at 0x7fd587f7cac8>, <Lv2Param object as value=0.5 [0.0 - 1.0] at 0x7fd587f7eba8>, <Lv2Param object as value=0.25 [0.0 - 2.0] at 0x7fd58c576c88>, <Lv2Param object as value=1.0 [0.0 - 2.0] at 0x7fd58c578d68>, <Lv2Param object as value=0.0 [0.0 - 500.0] at 0x7fd58c57ae80>, <Lv2Param object as value=300.0 [20.0 - 20000.0] at 0x7fd58c57df98>, <Lv2Param object as value=5000.0 [20.0 - 20000.0] at 0x7fd58c5810f0>)

        >>> param = my_awesome_effect.params[0]
        >>> param
        <Lv2Param object as value=1.5 [0.4000000059604645 - 15.0] at 0x7fd587f77908>

        >>> param.default
        1.5
        >>> param.value = 14

        >>> symbol = param.symbol
        >>> symbol
        'decay_time'
        >>> param == my_awesome_effect.params[symbol]
        True

    :param Effect effect: Effect in which this parameter belongs
    :param default: Default value (initial value parameter)
    """

    def __init__(self, effect, default):
        self._effect = effect
        self._value = default
        self._default = default

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
        Default parameter value.
        Then a effect is instanced, the value initial for a parameter is
        your default value.

        :getter: Default parameter value.
        """
        return self._default

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

        if not(self.minimum <= new_value <= self.maximum):
            msg = 'New value out of range: {} [{} - {}]'.format(
                new_value,
                self.minimum,
                self.maximum
            )
            raise ParamError(msg)

        self._value = new_value
        self.observer.on_param_value_changed(self)

    @property
    @abstractmethod
    def minimum(self):
        """
        :return: Smaller value that the parameter can assume
        """
        pass

    @property
    @abstractmethod
    def maximum(self):
        """
        :return: Greater value that the parameter can assume
        """
        pass

    @property
    @abstractmethod
    def symbol(self):
        """
        :return: Param identifier
        """
        pass

    def __repr__(self, *args, **kwargs):
        return "<{} object as value={} [{} - {}] at 0x{:x}>".format(
            self.__class__.__name__,
            self.value,
            self.minimum,
            self.maximum,
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
            'index': self.index,
            'symbol': self.symbol,
            'value': self.value,
            'minimum': self.minimum,
            'maximum': self.maximum,
        }

    @property
    def index(self):
        return self.effect.params.index(self)
