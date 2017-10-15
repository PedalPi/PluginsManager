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

from abc import ABCMeta

from pluginsmanager.model.port import Port


class MidiPort(Port, metaclass=ABCMeta):
    """
    Port is a parent abstraction for midi inputs and midi outputs
    """
    pass

    @property
    def connection_class(self):
        """
        :return MidiConnection: Class used for connections in this port
        """
        from pluginsmanager.model.midi_connection import MidiConnection
        return MidiConnection
