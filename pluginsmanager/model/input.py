from abc import ABCMeta

from unittest.mock import MagicMock


class Input(metaclass=ABCMeta):

    def __init__(self, effect):
        self._effect = effect

        self.observer = MagicMock()

    @property
    def effect(self):
        return self._effect

    @property
    def json(self):
        """
        Get a json decodable representation of this input

        :return dict: json representation
        """
        return self.__dict__

    @property
    def __dict__(self):
        return {
            'effect': self.effect.patch.effects.index(self.effect),
            'index': self.effect.inputs.index(self),
        }
