from pluginsmanager.util.observable_list import ObservableList
from pluginsmanager.model.update_type import UpdateType

from unittest.mock import MagicMock


class Patch(object):
    """
    Patch is a pedalboard representation: your structure contains
    :class:`Effect` and :class:`Connection`.

    :param string name: Patch name
    """
    def __init__(self, name):
        self.name = name
        self._effects = ObservableList()
        self._connections = ObservableList()

        self.effects.observer = self._effects_observer
        self.connections.observer = self._connections_observer

        self._observer = MagicMock()

        self.bank = None

    @property
    def observer(self):
        return self._observer

    @observer.setter
    def observer(self, observer):
        self._observer = observer

        for effect in self.effects:
            effect.observer = observer

    def _effects_observer(self, update_type, effect, index):
        kwargs = {
            'index': index,
            'origin': self
        }

        if update_type == UpdateType.CREATED \
        or update_type == UpdateType.UPDATED:
            effect.patch = self
            effect.observer = self.observer
        elif update_type == UpdateType.DELETED:
            for connection in effect.connections:
                self.connections.remove(connection)

            effect.patch = None
            effect.observer = MagicMock()

        self.observer.on_effect_updated(effect, update_type, **kwargs)

    def _connections_observer(self, update_type, connection, index):
        self.observer.on_connection_updated(connection, update_type)

    @property
    def json(self):
        """
        Get a json decodable representation of this patch

        :return dict: json representation
        """
        return self.__dict__

    @property
    def __dict__(self):
        return {
            'name': self.name,
            'effects': [effect.json for effect in self.effects],
            'connections': [connection.json for connection in self.connections]
        }

    def append(self, effect):
        """
        Add a :class:`Effect` in this patch

        This works same as::
        >>> patch.effects.append(effect)
        or::
        >>> patch.effects.insert(len(patch.effects), effect)

        :param Effect effect: Effect that will be added
        """
        self.effects.append(effect)

    @property
    def effects(self):
        return self._effects

    @property
    def connections(self):
        return self._connections