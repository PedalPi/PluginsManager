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

from pluginsmanager.model.audio_port import AudioPort


class Output(AudioPort, metaclass=ABCMeta):
    """
    Output is the medium in which the audio processed by the effect is returned.

    Effects usually have a one (mono) or two outputs (stereo L + stereo R). .

    For obtains the outputs::

        >>> my_awesome_effect
        <Lv2Effect object as 'Calf Reverb' active at 0x7fd58d874ba8>
        >>> my_awesome_effect.outputs
        (<Lv2Output object as Out L at 0x7fd58c58a438>, <Lv2Output object as Out R at 0x7fd58c58d550>)

        >>> output = my_awesome_effect.outputs[0]
        >>> output
        <Lv2Output object as Out L at 0x7fd58c58a438>

        >>> symbol = my_awesome_effect.outputs[0].symbol
        >>> symbol
        'output_l'

        >>> my_awesome_effect.outputs[symbol] == output
        True

    For connections between effects, see :meth:`~pluginsmanager.model.pedalboard.Pedalboard.connect()`
    and :meth:`~pluginsmanager.model.pedalboard.Pedalboard.disconnect()` :class:`.Pedalboard` class methods.

    :param Effect effect: Effect that contains the output
    """

    @property
    def index(self):
        """
        :return: Output index in the your effect
        """
        return self.effect.outputs.index(self)
