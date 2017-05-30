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

import socket


class Connection(object):
    """
    Class responsible for managing an API connection to the mod-host process via socket
    """
    client = None

    def __init__(self, socket_port=5555, address='localhost'):
        self.client = socket.socket()
        self.client.connect((address, socket_port))
        self.client.settimeout(5)

    def send(self, message):
        """
        Sends message to *mod-host*.

        .. note::

            Uses :class:`.ProtocolParser` for a high-level management.
            As example, view :class:`.Host`

        :param string message: Message that will be sent for *mod-host*
        """
        print(message.encode('utf-8'))
        self.client.send(message.encode('utf-8'))
        received = self.client.recv(1024)

        return received

    def close(self):
        """
        Closes socket connection
        """
        self.client.close()
