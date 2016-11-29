from pluginsmanager.model.input import Input


class Lv2Input(Input):
    """
    Representation of a Lv2 `input audio port`_ instance.

    For general input use, see :class:`Input` class documentation.

    .. _input audio port: http://lv2plug.in/ns/lv2core/#InputPort

    :param Lv2Effect effect:
    :param dict effect_input: *input audio port* json representation
    """

    def __init__(self, effect, effect_input):
        super(Lv2Input, self).__init__(effect)
        self._input = effect_input

    def __str__(self):
        return self._input['name']

    def __repr__(self):
        return "<{} object as {} at 0x{:x}>".format(
            self.__class__.__name__,
            str(self),
            id(self)
        )

    @property
    def symbol(self):
        return self._input['symbol']

    @property
    def __dict__(self):
        dictionary = super(Lv2Input, self).__dict__
        dictionary['index'] = self._input['index']

        return dictionary
