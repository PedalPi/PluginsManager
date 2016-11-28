from abc import ABCMeta, abstractmethod

from pluginsmanager.model.connection import Connection

from unittest.mock import MagicMock


class Output(metaclass=ABCMeta):
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

    For connections between effects, view :class:`Connections`.

    :param Effect effect: Effect of output
    """

    def __init__(self, effect):
        self._effect = effect

        self.observer = MagicMock()

    @property
    def effect(self):
        """
        :return: Effect of output
        """
        return self._effect

    def connect(self, effect_input):
        """
        Connect it with effect_input::

            >>> driver_output = driver.outputs[0]
            >>> reverb_input = reverb.inputs[0]
            >>> Connection(driver_output, reverb_input) in driver.effect.connections
            False
            >>> driver_output.connect(reverb_input)
            >>> Connection(driver_output, reverb_input) in driver.effect.connections
            True

        :param Input effect_input: Input that will be connected with it
        """
        self.effect.patch.connections.append(Connection(self, effect_input))

    def disconnect(self, effect_input):
        """
        Disconnect it with effect_input

            >>> driver_output = driver.outputs[0]
            >>> reverb_input = reverb.inputs[0]
            >>> Connection(driver_output, reverb_input) in driver.effect.connections
            True
            >>> driver_output.disconnect(reverb_input)
            >>> Connection(driver_output, reverb_input) in driver.effect.connections
            False

        :param Input effect_input: Input that will be disconnected with it
        """
        self.effect.patch.connections.remove(Connection(self, effect_input))

    @property
    @abstractmethod
    def symbol(self):
        """
        :return: Output identifier
        """
        pass

    @property
    def json(self):
        """
        Get a json decodable representation of this output

        :return dict: json representation
        """
        return self.__dict__

    @property
    def __dict__(self):
        return {
            'effect': self.effect.patch.effects.index(self.effect),
            'symbol': self.symbol,
            'index': self.effect.outputs.index(self),
        }
