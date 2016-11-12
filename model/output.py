from abc import ABCMeta

from model.connection import Connection

from unittest.mock import MagicMock


class Output(metaclass=ABCMeta):

    def __init__(self, effect):
        self._effect = effect

        self.observer = MagicMock()

    @property
    def effect(self):
        return self._effect

    def connect(self, input):
        self.effect.patch.connections.append(Connection(self, input))

    def disconnect(self, input):
        self.effect.patch.connections.remove(Connection(self, input))

    @property
    def json(self):
        """
        Get a json decodable representation of this output

        :return dict: json representation
        """
        return self.__dict__

    @property
    def __dict__(self):
        return {
            'effect': self.effect.patch.effects.index(self.effect),
            'index': self.effect.outputs.index(self),
        }
