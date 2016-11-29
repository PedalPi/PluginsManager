from pluginsmanager.model.output import Output


class Lv2Output(Output):
    """
    Representation of a Lv2 `output audio port`_ instance.

    For general input use, see :class:`Output` class documentation.

    .. _output audio port: http://lv2plug.in/ns/lv2core/#OutputPort
    http://lv2plug.in/ns/lv2core/#Parameter

    :param Lv2Effect effect:
    :param dict effect_output: *output audio port* json representation
    """

    def __init__(self, effect, effect_output):
        super(Lv2Output, self).__init__(effect)
        self._output = effect_output

    def __str__(self):
        return self._output['name']

    def __repr__(self):
        return "<{} object as {} at 0x{:x}>".format(
            self.__class__.__name__,
            str(self),
            id(self)
        )

    @property
    def symbol(self):
        return self._output['symbol']

    @property
    def __dict__(self):
        dictionary = super(Lv2Output, self).__dict__
        dictionary['index'] = self._output['index']

        return dictionary
