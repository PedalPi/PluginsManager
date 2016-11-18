from pluginsmanager.model.input import Input


class Lv2Input(Input):

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
    def __dict__(self):
        dictionary = super(Lv2Input, self).__dict__
        dictionary['index'] = self._input['index']
        dictionary['symbol'] = self._input['symbol']

        return dictionary
