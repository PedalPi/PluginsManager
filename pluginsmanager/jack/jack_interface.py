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

import pyaudio


class JackInterfaces(object):
    """
    JackInterface extract informations about the audio interfaces in the system.

    Requires `pyaudio`_. In Debian based systems, install using::

        sudo apt-get install portaudio19-dev python-all-dev
        pip install pyaudio

    .. _pyaudio: https://people.csail.mit.edu/hubert/pyaudio/
    """

    @staticmethod
    def audio_interfaces():
        """
        Extracts audio interfaces data

        :return list[AudioInterface]: Audio interfaces data
        """
        p = pyaudio.PyAudio()

        interfaces = []
        for i in range(p.get_device_count()):
            data = p.get_device_info_by_index(i)
            if 'hw' not in data['name']:
                interfaces.append(AudioInterface(data))

        p.terminate()

        return interfaces


class AudioInterface(object):
    """
    JackInterface contains data about a audio interface

    :param data: PyAudio interface data using `py_audio_instance.get_device_info_by_index(i)`
    """
    def __init__(self, data):
        self._data = data

    @property
    def data(self):
        """
        :return dict: Original PyAudio interface data
        """
        return self._data

    @property
    def name(self):
        """
        :return string: Device name
        """
        return self.data['name'].split('(')[0]

    @property
    def hw(self):
        """
        :return string: String informing hardware card index and device index
                        Example: `'hw:1:0'`
        """
        return self.data['name'].split('(')[1][0:-1]

    @property
    def total_inputs(self):
        """
        :return float: Max input channels in this audio interface
        """
        return self.data['maxInputChannels']

    @property
    def total_outputs(self):
        """
        :return float: Max output channels in this audio interface
        """
        return self.data['maxOutputChannels']

    @property
    def latency(self):
        """
        :return dict: Min and Max default latency for input and output channels
        """
        return {
            'input': {
                'min': self.data['defaultLowInputLatency'],
                'max': self.data['defaultHighInputLatency'],
            },
            'output': {
                'min': self.data['defaultLowOutputLatency'],
                'max': self.data['defaultHighOutputLatency'],
            }
        }

    @property
    def default_sample_rate(self):
        return self.data['defaultSampleRate']

    @property
    def json(self):
        """
        Get a json decodable representation of this JackInterface

        :return dict: json representation
        """
        return self.__dict__

    @property
    def __dict__(self):
        return {
            'name': self.name,
            'hw': self.hw,
            'total_inputs': self.total_inputs,
            'total_outputs': self.total_outputs,
            'latency': self.latency,
            'default_sample_rate': self.default_sample_rate
        }
