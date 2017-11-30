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

from pluginsmanager.model.connection import Connection
from pluginsmanager.model.midi_port import MidiPort


class MidiConnection(Connection):
    """
    :class:`.MidiConnection` represents a connection between two
    distinct effects by your :class:`.MidiPort` (effect :class:`.MidiOutput` with effect :class:`.MidiInput`)::

    >>> californication = Pedalboard('Californication')
    >>> californication.append(driver)
    >>> californication.append(reverb)

    >>> output_port = cctonode1.midi_outputs[0]
    >>> input_port = cctonode2.midi_inputs[0]

    >>> californication.connections.append(MidiConnection(output_port, input_port))

    Another way to use implicitly connections::

    >>> californication.connect(output_port, input_port)

    :param MidiOutput output_port: MidiOutput port that will be connected with midi input port
    :param MidiInput input_port: MidiInput port that will be connected with midi output port
    """

    @property
    def ports_class(self):
        """
        :return class: Port class that this connection only accepts
        """
        return MidiPort

    @property
    def __dict__(self):
        dictionary = super(MidiConnection, self).__dict__
        dictionary['type'] = 'midi'

        return dictionary
