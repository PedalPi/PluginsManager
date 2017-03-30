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

from pluginsmanager.mod_host.connection import Connection
from pluginsmanager.mod_host.protocol_parser import ProtocolParser


class Host:
    """
    Bridge between *mod-host* API and *mod-host* process
    """

    def __init__(self, address='localhost'):
        # mod-host works only exists 2 connections:
        #  - For communication
        self.connection = Connection(5555, address)
        #  - For callback?
        self.connection_fd = Connection(5556, address)

        self.instance_index = 0

    def add(self, effect):
        """
        Add an LV2 plugin encapsulated as a jack client

        :param Lv2Effect effect: Effect that will be loaded as LV2 plugin encapsulated
        """
        effect.instance = self.instance_index
        self.instance_index += 1

        self.connection.send(ProtocolParser.add(effect))

    def remove(self, effect):
        """
        Remove an LV2 plugin instance (and also the jack client)

        :param Lv2Effect effect: Effect that your jack client encapsulated will removed
        """
        self.connection.send(ProtocolParser.remove(effect))

    def connect_input_in(self, effect_input):
        """
        .. deprecated:: 0.0

           Will be removed
        """
        self.connection.send(ProtocolParser.connect_input_in(effect_input))

    def connect_on_output(self, effect_output, index_out):
        """
        .. deprecated:: 0.0

           Will be removed
        """
        self.connection.send(ProtocolParser.connect_on_output(effect_output, index_out))

    def connect(self, connection):
        """
        Connect two effect audio ports

        :param pluginsmanager.model.connection.Connection connection: Connection with the two effect audio ports (output and input)
        """
        self.connection.send(ProtocolParser.connect(connection))

    def disconnect(self, connection):
        """
        Disconnect two effect audio ports

        :param pluginsmanager.model.connection.Connection connection: Connection with the two effect audio ports (output and input)
        """
        self.connection.send(ProtocolParser.disconnect(connection))

    def set_param_value(self, param):
        """
        Set a value to given control

        :param Lv2Param param: Param that the value will be updated
        """
        self.connection.send(ProtocolParser.param_set(param))

    def set_status(self, effect):
        """
        Toggle effect processing

        :param Lv2Effect effect: Effect with the status updated
        """
        self.connection.send(ProtocolParser.bypass(effect))
