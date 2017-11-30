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


class Port(metaclass=ABCMeta):
    """
    Port is a parent abstraction for inputs and outputs

    :param Effect effect: Effect that contains port
    """

    def __init__(self, effect):
        self._effect = effect
        self.observer = MagicMock()

    @property
    @abstractmethod
    def symbol(self):
        """
        :return: Identifier for this port
        """
        pass

    @property
    def effect(self):
        """
        :return: Effect that this port is related
        """
        return self._effect

    @property
    def json(self):
        """
        Get a json decodable representation

        :return dict: json representation
        """
        return self.__dict__

    @property
    @abstractmethod
    def index(self):
        """
        :return: Index in the effect related based in your category.
                 As example, if this port is a :class:`input`, the
                 index returns your position in the inputs ports.
        """
        pass

    @property
    def __dict__(self):
        return {
            'effect': self.effect.index,
            'symbol': self.symbol,
            'index': self.index,
        }

    def __repr__(self):
        return "<{} object as {} at 0x{:x}>".format(
            self.__class__.__name__,
            str(self),
            id(self)
        )

    @property
    @abstractmethod
    def connection_class(self):
        """
        :return: Class used for connections in this port
        """
        pass
