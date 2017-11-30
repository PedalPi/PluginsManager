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
    Automatic system physical ports detection.

    Maybe the midi ports not will recognize. In these cases,
    you need to start `a2jmidid`_ to get MIDI-ALSA ports automatically
    mapped to JACK-MIDI ports.

    .. _a2jmidid: http://manual.ardour.org/setting-up-your-system/setting-up-midi/midi-on-linux/

    :param JackClient jack_client: :class:`.JackClient` instance that will get the information to
                                   generate :class:`.SystemEffect`
    """
    def __init__(self, jack_client):
        self.client = jack_client

    def build(self):
        inputs  = (port.shortname for port in self.client.audio_inputs)
        outputs = (port.shortname for port in self.client.audio_outputs)
        midi_inputs  = (port.shortname for port in self.client.midi_inputs)
        midi_outputs = (port.shortname for port in self.client.midi_outputs)

        return SystemEffect('system', outputs, inputs, midi_outputs, midi_inputs)
