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

from pluginsmanager.model.connection import Connection, ConnectionError

from unittest.mock import MagicMock


class Output(metaclass=ABCMeta):
    """
    Output is the medium in which the audio processed by the effect is returned.

    Effects usually have a one (mono) or two outputs (stereo L + stereo R). .

    For obtains the outputs::

        >>> my_awesome_effect
        <Lv2Effect object as 'Calf Reverb' active at 0x7fd58d874ba8>
        >>> my_awesome_effect.outputs
        (<Lv2Output object as Out L at 0x7fd58c58a438>, <Lv2Output object as Out R at 0x7fd58c58d550>)

        >>> output = my_awesome_effect.outputs[0]
        >>> output
        <Lv2Output object as Out L at 0x7fd58c58a438>

        >>> symbol = my_awesome_effect.outputs[0].symbol
        >>> symbol
        'output_l'

        >>> my_awesome_effect.outputs[symbol] == output
        True

    For connections between effects, view :class:`.pluginsmanager.mod_host.connection.Connection`.

    :param Effect effect: Effect that contains the output
    """

    def __init__(self, effect):
        self._effect = effect

        self.observer = MagicMock()

        self._unique_for_all_pedalboards = False

    @property
    def effect(self):
        """
        :return: Effect of output
        """
        return self._effect

    def connect(self, effect_input):
        """
        Connect it with effect_input::

            >>> driver_output = driver.outputs[0]
            >>> reverb_input = reverb.inputs[0]
            >>> Connection(driver_output, reverb_input) in driver.effect.connections
            False
            >>> driver_output.connect(reverb_input)
            >>> Connection(driver_output, reverb_input) in driver.effect.connections
            True

        .. note::

            This method does not work for all cases.
            class:`SystemOutput` can not be connected with class:`SystemInput` this way.
            For this case, use ::

                >>> pedalboard.connections.append(Connection(system_output, system_input))

        :param Input effect_input: Input that will be connected with it
        """
        if self._unique_for_all_pedalboards and effect_input._unique_for_all_pedalboards:
            error = "Isn't possible connect this way. Please use pedalboard.connect(Connection(output, input))"
            raise ConnectionError(error)

        pedalboard = self.effect.pedalboard if not self._unique_for_all_pedalboards else effect_input.effect.pedalboard
        pedalboard.connections.append(Connection(self, effect_input))

    def disconnect(self, effect_input):
        """
        Disconnect it with effect_input

            >>> driver_output = driver.outputs[0]
            >>> reverb_input = reverb.inputs[0]
            >>> Connection(driver_output, reverb_input) in driver.effect.connections
            True
            >>> driver_output.disconnect(reverb_input)
            >>> Connection(driver_output, reverb_input) in driver.effect.connections
            False

        .. note::

            This method does not work for all cases.
            class:`SystemOutput` can not be disconnected with class:`SystemInput` this way.
            For this case, use ::

                >>> pedalboard.connections.remove(Connection(system_output, system_input))

        :param Input effect_input: Input that will be disconnected with it
        """
        if self._unique_for_all_pedalboards and effect_input._unique_for_all_pedalboards:
            error = "Isn't possible connect this way. Please use pedalboard.connect(Connection(output, input))"
            raise ConnectionError(error)

        self.effect.pedalboard.connections.remove(Connection(self, effect_input))

    @property
    @abstractmethod
    def symbol(self):
        """
        :return: Output identifier
        """
        pass

    @property
    def json(self):
        """
        Get a json decodable representation of this output

        :return dict: json representation
        """
        return self.__dict__

    @property
    def __dict__(self):
        return {
            'effect': self.effect.index,
            'symbol': self.symbol,
            'index': self.index,
        }

    @property
    def index(self):
        """
        :return Output index in the your effect
        """
        return self.effect.outputs.index(self)
