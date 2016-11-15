

class ConnectionError(Exception):
    def __init__(self, message):
        super(ConnectionError, self).__init__(message)
        self.message = message


class Connection(object):
    """
    :class:`Connection` represents a connection between two
    distinct effects

    :param Output effect_output:
    :param Input effect_input:
    """

    def __init__(self, effect_output, effect_input):
        if effect_output.effect == effect_input.effect:
            ConnectionError('Effect of output and effect of input are equals')

        self._output = effect_output
        self._input = effect_input

    @property
    def output(self):
        return self._output

    @property
    def input(self):
        return self._input

    def __eq__(self, other):
        return isinstance(other, self.__class__) \
           and self.input == other.input \
           and self.output == other.output

    def __repr__(self):
        return "<{} object as '{}.{} -> {}.{}' at 0x{:x}>".format(
            self.__class__.__name__,
            self.output.effect,
            self.output,
            self.input.effect,
            self.input,
            id(self)
        )

    @property
    def json(self):
        """
        Get a json decodable representation of this effect

        :return dict: json representation
        """
        return self.__dict__

    @property
    def __dict__(self):
        return {
            'output': self.output.json,
            'input': self.input.json,
        }
