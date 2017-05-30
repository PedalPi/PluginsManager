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


class ConnectionError(Exception):
    def __init__(self, message):
        super(ConnectionError, self).__init__(message)
        self.message = message


class Connection(object):
    """
    :class:`pluginsmanager.model.connection.Connection` represents a connection between two
    distinct effects by your ports (effect :class:`.Output` with effect :class:`.Input`)::

    >>> californication = Pedalboard('Californication')
    >>> californication.append(driver)
    >>> californication.append(reverb)

    >>> guitar_output = sys_effect.outputs[0]
    >>> driver_input = driver.inputs[0]
    >>> driver_output = driver.outputs[0]
    >>> reverb_input = reverb.inputs[0]
    >>> reverb_output = reverb.outputs[0]
    >>> amp_input = sys_effect.inputs[0]

    >>> # Guitar -> driver -> reverb -> amp
    >>> californication.connections.append(Connection(guitar_output, driver_input))
    >>> californication.connections.append(Connection(driver_output, reverb_input))
    >>> californication.connections.append(Connection(reverb_output, amp_input))

    Another way to use implicitly connections::

    >>> guitar_output.connect(driver_input)
    >>> driver_output.connect(reverb_input)
    >>> reverb_output.connect(amp_input)

    :param Output effect_output: Output port that will be connected with input port
    :param Input effect_input: Input port that will be connected with output port
    """

    def __init__(self, effect_output, effect_input):
        if effect_output.effect == effect_input.effect\
        and not effect_output.effect.is_possible_connect_itself:
            raise ConnectionError('Effect of output and effect of input are equals')

        self._output = effect_output
        self._input = effect_input

    @property
    def output(self):
        """
        :return Output: Output connection port
        """
        return self._output

    @property
    def input(self):
        """
        :return Output: Input connection port
        """
        return self._input

    def __eq__(self, other):
        return isinstance(other, self.__class__) \
           and self.input == other.input \
           and self.output == other.output

    def __repr__(self):
        return "<{} object as '{}.{} -> {}.{}' at 0x{:x}>".format(
            self.__class__.__name__,
            self.output.effect,
            self.output,
            self.input.effect,
            self.input,
            id(self)
        )

    @property
    def json(self):
        """
        Get a json decodable representation of this effect

        :return dict: json representation
        """
        return self.__dict__

    @property
    def __dict__(self):
        return {
            'output': self.output.json,
            'input': self.input.json,
        }
