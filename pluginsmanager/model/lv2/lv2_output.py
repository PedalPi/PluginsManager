from pluginsmanager.model.output import Output


class Lv2Output(Output):

    def __init__(self, effect, output):
        super(Lv2Output, self).__init__(effect)
        self._output = output

    def __str__(self):
        return self._output['name']

    def __repr__(self):
        return "<{} object as {} at 0x{:x}>".format(
            self.__class__.__name__,
            str(self),
            id(self)
        )

    @property
    def __dict__(self):
        dictionary = super(Lv2Output, self).__dict__
        dictionary['index'] = self._output['index']
        dictionary['symbol'] = self._output['symbol']

        return dictionary
