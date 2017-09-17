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

import logging

from pluginsmanager.observer.mod_host.connection import Connection
from pluginsmanager.observer.mod_host.protocol_parser import ProtocolParser


class Host:
    """
    Bridge between *mod-host* API and *mod-host* process
    """

    def __init__(self, address='localhost', port=5555):
        self.connection = None
        self.connection_fd = None

        # mod-host works if only exists two connections:
        #  - For communication
        try:
            self.connection = Connection(port, address)
        except ConnectionRefusedError as e:
            raise ConnectionRefusedError(str(e) + '. Do you starts mod-host?') from e

        #  - For callback?
        try:
            self.connection_fd = Connection(port+1, address)
        except ConnectionRefusedError as e:
            logging.info('Mod-host - Feedback socket is not enabled')
            logging.info('           Try start Mod-host using: mod-host -f {}'.format(port+1))

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

    def quit(self):
        """
        Quit the connection with mod-host and
        stop the mod-host process
        """
        self.connection.send(ProtocolParser.quit())
        self.close()

    def close(self):
        """
        Quit the connection with mod-host
        """
        if self.connection is not None:
            self.connection.close()
        if self.connection_fd is not None:
            self.connection_fd.close()
