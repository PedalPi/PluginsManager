from model.input import Input


class Lv2Input(Input):

    def __init__(self, effect, input):
        super(Lv2Input, self).__init__(effect)
        self._input = input

    def __str__(self):
        return self._input['name']

    def __repr__(self):
        return "<{} object as {} at 0x{:x}>".format(
            self.__class__.__name__,
            str(self),
            id(self)
        )

    @property
    def __dict__(self):
        dictonary = super(Lv2Input, self).__dict__
        dictonary['index'] = self._input['index']
        dictonary['symbol'] = self._input['symbol']

        return dictonary
