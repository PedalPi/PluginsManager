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

from abc import ABCMeta, abstractmethod


class AudioPortBuilder(metaclass=ABCMeta):
    """
    Extracts the inputs and outputs of an effect defined in a json.

    Use it to get the `AudioPorts`_ (inputs and outputs) to build a connection correctly.

    .. _AudioPorts: http://lv2plug.in/ns/lv2core/#AudioPort
    """

    @abstractmethod
    def build_input(self, json):
        """
        :return Input: Input of an effect defined in json
        """
        pass

    @abstractmethod
    def build_output(self, json):
        """
        :return Output: Output of an effect defined in json
        """
        pass

    @abstractmethod
    def build_midi_input(self, json):
        """
        :return MidiInput: MidiInput of an effect defined in json
        """
        pass

    @abstractmethod
    def build_midi_output(self, json):
        """
        :return MidiOutput: MidiOutput of an effect defined in json
        """
        pass


class EffectBuilder(metaclass=ABCMeta):

    @abstractmethod
    def build(self, json):
        pass
