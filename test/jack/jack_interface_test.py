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

import unittest

from pluginsmanager.jack.jack_interface import JackInterfaces, AudioInterface


class JackInterfaceTest(unittest.TestCase):

    def test_list_audio_interfaces(self):
        """Assert not raises error"""
        audio_interfaces = JackInterfaces.audio_interfaces()
        self.assertTrue(len(audio_interfaces) >= 0)

    def test_audio_interface(self):
        pyaudio_data = {
            'defaultHighInputLatency': -1.0,
            'defaultHighOutputLatency': 0.034829931972789115,
            'defaultLowInputLatency': -1.0,
            'defaultLowOutputLatency': 0.005804988662131519,
            'defaultSampleRate': 44100.0,
            'hostApi': 0,
            'index': 1,
            'maxInputChannels': 0,
            'maxOutputChannels': 2,
            'name': 'bcm2835 ALSA: IEC958/HDMI (hw:0,1)',
            'structVersion': 2
        }

        correct_data = {
            'name': 'bcm2835 ALSA: IEC958/HDMI ',
            'hw': 'hw:0,1',
            'total_inputs': 0,
            'total_outputs': 2,
            'latency': {
                'input': {
                    'min': -1.0,
                    'max': -1.0,
                },
                'output': {
                    'min': 0.005804988662131519,
                    'max': 0.034829931972789115,
                }
            },
            'default_sample_rate': 44100.0
        }

        interface = AudioInterface(pyaudio_data)

        self.assertDictEqual(pyaudio_data, interface.data)
        self.assertDictEqual(correct_data, interface.json)
