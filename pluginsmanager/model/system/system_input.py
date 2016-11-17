from pluginsmanager.model.input import Input


class SystemInput(Input):

    def __init__(self, effect, input):
        super(SystemInput, self).__init__(effect)
        self._input = input

    def __str__(self):
        return self._input

    def __repr__(self):
        return "<{} object as {} at 0x{:x}>".format(
            self.__class__.__name__,
            str(self),
            id(self)
        )

    @property
    def __dict__(self):
        dictionary = {}
        dictionary['symbol'] = str(self)

        return dictionary
