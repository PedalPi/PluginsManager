from pluginsmanager.model.effect import Effect
from pluginsmanager.model.system.system_input import SystemInput
from pluginsmanager.model.system.system_output import SystemOutput


class SystemEffect(Effect):
    """
    Representation of the system instance (audio cards).

    System output is equivalent with audio input: You connect the
    instrument in the audio card input and it captures and send the
    audio to :class:`SystemOutput` for you connect in a input plugins.

    System input is equivalent with audio output: The audio card receives
    the audio processed in your :class:`SystemInput` and send it to audio
    card output for you connects in amplifier, headset.

    Because no autodetection of existing ports in audio card
    has been implemented, you must explicitly inform in the
    creation of the SystemEffect object::

    >>> sys_effect = SystemEffect('system', ('capture_1', 'capture_2'), ('playback_1', 'playback_2'))

    Unlike effects that should be added in the patch, SystemEffects MUST NOT::

    >>> builder = Lv2EffectBuilder()

    >>> patch = Patch('Rocksmith')
    >>> reverb = builder.build('http://calf.sourceforge.net/plugins/Reverb')
    >>> patch.append(reverb)

    However the patch must have the connections::

    >>> patch.connections.append(Connection(sys_effect.outputs[0], reverb.inputs[0]))

    An bypass example::

    >>> patch = Patch('Bypass example')
    >>> sys_effect = SystemEffect('system', ('capture_1', 'capture_2'), ('playback_1', 'playback_2'))
    >>> patch.connections.append(Connection(sys_effect.outputs[0], sys_effect.inputs[0]))
    >>> patch.connections.append(Connection(sys_effect.outputs[1], sys_effect.inputs[1]))

    :param string representation: Audio card representation. Usually 'system'
    :param tuple(string) outputs: Tuple of outputs representation. Usually a output representation
                                  starts with `capture_`
    :param tuple(string) inputs: Tuple of inputs representation. Usually a input representation
                                 starts with `playback_`
    """
    def __init__(self, representation, outputs, inputs):
        super(SystemEffect, self).__init__()

        self.representation = representation

        self._params = tuple()
        self._inputs = tuple([SystemInput(self, effect_input) for effect_input in inputs])
        self._outputs = tuple([SystemOutput(self, effect_output) for effect_output in outputs])

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

    def __str__(self):
        return self.representation

    def __repr__(self):
        return "<{} object as '{}' at 0x{:x}>".format(
            self.__class__.__name__,
            str(self),
            id(self)
        )

    @property
    def __dict__(self):
        return {
            'technology': 'system',
        }
