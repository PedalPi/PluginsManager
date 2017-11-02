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


from pluginsmanager.model.audio_port import AudioPort


class ConnectionError(Exception):
    def __init__(self, message):
        super(ConnectionError, self).__init__(message)
        self.message = message


class Connection(object):
    """
    :class:`~pluginsmanager.model.connection.Connection` represents a connection between two
    distinct effects by your :class:`.AudioPort` (effect :class:`.Output` with effect :class:`.Input`)::

    >>> from pluginsmanager.model.pedalboard import Pedalboard
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

    >>> californication.connect(guitar_output, driver_input)
    >>> californication.connect(driver_output, reverb_input)
    >>> californication.connect(reverb_output, amp_input)

    :param Output output_port: Audio output port that will be connected with audio input port
    :param Input input_port: Audio input port that will be connected with audio output port
    """

    def __init__(self, output_port, input_port):
        if not self._valid_instance(output_port)\
        or not self._valid_instance(input_port):
            raise ConnectionError("'{}' only accepts ports that inherits {}".format(self.__class__.__name__, self.ports_class.__name__))

        if output_port.effect == input_port.effect\
        and not output_port.effect.is_possible_connect_itself:
            effect_name = str(input_port.effect)
            raise ConnectionError("The output {} and input {} are from the same effect {}. "
                                  "This effect doesn't accept connections between itself instance."
                                  .format(effect_name, str(output_port), str(input_port)))

        self._output = output_port
        self._input = input_port

    def _valid_instance(self, port):
        return isinstance(port, self.ports_class)

    @property
    def ports_class(self):
        """
        :return class: Port class that this connection only accepts
        """
        return AudioPort

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
            'type': 'audio'
        }

    def __hash__(self):
        return '{} x {}'.format(self.output, self.input).__hash__()
