from pluginsmanager.model.output import Output


class SystemOutput(Output):

    def __init__(self, effect, output):
        super(SystemOutput, self).__init__(effect)
        self._output = output
        self._unique_for_all_pedalboards = True

    def __str__(self):
        return self._output

    def __repr__(self):
        return "<{} object as {} at 0x{:x}>".format(
            self.__class__.__name__,
            str(self),
            id(self)
        )

    @property
    def symbol(self):
        return str(self)

    @property
    def __dict__(self):
        return {
            'symbol': self.symbol,
            'index': self.effect.outputs.index(self),
        }
