from pluginsmanager.model.output import Output


class SystemOutput(Output):

    def __init__(self, effect, output):
        super(SystemOutput, self).__init__(effect)
        self._output = output

    def __str__(self):
        return self._output

    def __repr__(self):
        return "<{} object as {} at 0x{:x}>".format(
            self.__class__.__name__,
            str(self),
            id(self)
        )

    @property
    def __dict__(self):
        dictionary = super(SystemOutput, self).__dict__
        del dictionary['index']
        dictionary['symbol'] = str(self)

        return dictionary
