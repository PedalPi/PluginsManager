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
from unittest.mock import MagicMock

from pluginsmanager.util.dict_tuple import DictTuple


class Effect(metaclass=ABCMeta):
    """
    Representation of a audio plugin instance - LV2 plugin encapsulated as a jack client.

    Effect contains a `active` status (off=bypass), a list of :class:`.Param`,
    a list of :class:`.Input` and a list of :class:`~pluginsmanager.model.connection.Connection`::

        >>> reverb = builder.build('http://calf.sourceforge.net/plugins/Reverb')
        >>> pedalboard.append(reverb)
        >>> reverb
        <Lv2Effect object as 'Calf Reverb' active at 0x7fd58d874ba8>

        >>> reverb.active
        True
        >>> reverb.toggle()
        >>> reverb.active
        False
        >>> reverb.active = True
        >>> reverb.active
        True

        >>> reverb.inputs
        (<Lv2Input object as In L at 0x7fd58c583208>, <Lv2Input object as In R at 0x7fd58c587320>)
        >>> reverb.outputs
        (<Lv2Output object as Out L at 0x7fd58c58a438>, <Lv2Output object as Out R at 0x7fd58c58d550>)
        >>> reverb.params
        (<Lv2Param object as value=1.5 [0.4000000059604645 - 15.0] at 0x7fd587f77908>, <Lv2Param object as value=5000.0 [2000.0 - 20000.0] at 0x7fd587f7a9e8>, <Lv2Param object as value=2 [0 - 5] at 0x7fd587f7cac8>, <Lv2Param object as value=0.5 [0.0 - 1.0] at 0x7fd587f7eba8>, <Lv2Param object as value=0.25 [0.0 - 2.0] at 0x7fd58c576c88>, <Lv2Param object as value=1.0 [0.0 - 2.0] at 0x7fd58c578d68>, <Lv2Param object as value=0.0 [0.0 - 500.0] at 0x7fd58c57ae80>, <Lv2Param object as value=300.0 [20.0 - 20000.0] at 0x7fd58c57df98>, <Lv2Param object as value=5000.0 [20.0 - 20000.0] at 0x7fd58c5810f0>)

    :param Pedalboard pedalboard: Pedalboard where the effect lies.
    """

    def __init__(self):
        self.pedalboard = None
        self._active = True

        self._params = ()
        self._inputs = DictTuple([], lambda: None)
        self._outputs = DictTuple([], lambda: None)
        self._midi_inputs = DictTuple([], lambda: None)
        self._midi_outputs = DictTuple([], lambda: None)

        self._observer = MagicMock()

    @property
    def observer(self):
        return self._observer

    @observer.setter
    def observer(self, observer):
        self._observer = observer

        for param in self.params:
            param.observer = self.observer

    @property
    def params(self):
        """
        :return list[Param]: Params of effect
        """
        return self._params

    @property
    def inputs(self):
        """
        :return list[Input]: Inputs of effect
        """
        return self._inputs

    @property
    def outputs(self):
        """
        :return list[Output]: Outputs of effect
        """
        return self._outputs

    @property
    def midi_inputs(self):
        """
        :return list[MidiInput]: MidiInputs of effect
        """
        return self._midi_inputs

    @property
    def midi_outputs(self):
        """
        :return list[MidiOutput]: MidiOutputs of effect
        """
        return self._midi_outputs

    @property
    def active(self):
        """
        Effect status: active or bypass

        :getter: Current effect status
        :setter: Set the effect Status
        :type: bool
        """
        return self._active

    @active.setter
    def active(self, status):
        if status == self._active:
            return

        self._active = status
        self.observer.on_effect_status_toggled(self)

    def toggle(self):
        """
        Toggle the effect status: ``self.active = not self.active``
        """
        self.active = not self.active

    @property
    def connections(self):
        """
        :return list[Connection]: Connections that this effects is present (with input or output port)
        """
        function = lambda connection: connection.input.effect == self \
                                   or connection.output.effect == self

        return tuple([c for c in self.pedalboard.connections if function(c)])

    @property
    def json(self):
        """
        Get a json decodable representation of this effect

        :return dict: json representation
        """
        return self.__dict__

    @property
    @abstractmethod
    def __dict__(self):
        pass

    @property
    def index(self):
        """
        Returns the first occurrence of the effect in your pedalboard
        """
        if self.pedalboard is None:
            raise IndexError('Effect not contains a pedalboard')

        return self.pedalboard.effects.index(self)

    @property
    def is_possible_connect_itself(self):
        """
        return bool: Is possible connect the with it self?
        """
        return False

    @property
    def is_unique_for_all_pedalboards(self):
        """
        return bool: Is unique for all pedalboards?
                     Example: :class:`.SystemEffect` is unique for all pedalboards
        """
        return False

    @property
    def use_real_identifier(self):
        """
        Instances of audio plugins are dynamically created, so the effect identifier for the jack can be set.

        However, SystemEffect correspond (mostly) to the audio interfaces already present in the computational system.
        The identifier for their jack has already been set.

        return bool: For this audio plugin, is necessary use the real effect identifier?
                     Example: :class:`.Lv2Effect` is False
                     Example: :class:`.SystemEffect` is True
        """
        return False

    def __repr__(self):
        return "<{} object as '{}' at 0x{:x}>".format(
            self.__class__.__name__,
            str(self),
            id(self)
        )

    @property
    def version(self):
        """
        :return string: Effect version
        """
        return ''
