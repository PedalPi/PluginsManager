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

from pluginsmanager.model.system.system_effect import SystemEffect


class SystemEffectBuilder(object):
    """
    Automatic system physical ports detection

    :param JackClient jack_client: :class:`.JackClient` instance that will get the information to
                                   generate :class:`.SystemEffect`
    """
    def __init__(self, jack_client):
        self.client = jack_client

    def build(self):
        inputs = []
        outputs = []

        for port in self.client.client.get_ports(is_audio=True, is_physical=True):
            if port.is_input:
                inputs.append(port.shortname)
            else:
                outputs.append(port.shortname)

        return SystemEffect('system', tuple(outputs), tuple(inputs))
