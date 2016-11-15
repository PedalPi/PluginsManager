from abc import ABCMeta, abstractmethod

from unittest.mock import MagicMock


class Effect(metaclass=ABCMeta):
    """
    Representation of a audio plugin instance.

    Effect contains a `active` status (off=bypass), a list of :class:`Param`,
    a list of :class:`Input` and a list of :class:`Connection`
    """

    def __init__(self, patch=None):
        self.patch = patch
        self._active = True

        self._observer = MagicMock()

    @property
    def observer(self):
        return self._observer

    @observer.setter
    def observer(self, observer):
        self._observer = observer

        for param in self.params:
            param.observer = self.observer

    @property
    @abstractmethod
    def params(self):
        """
        :return list[Param]: Params of effect
        """
        ...

    @property
    @abstractmethod
    def inputs(self):
        """
        :return list[Input]: Inputs of effect
        """
        ...

    @property
    @abstractmethod
    def outputs(self):
        """
        :return list[Output]: Outputs of effect
        """
        ...

    @property
    def active(self):
        """
        Is effect active?
        ``Active false = Inactive = bypass``

        :return bool: Effect status.
        """
        return self._active

    @active.setter
    def active(self, status):
        """
        Set effect status

        :param bool status: Effect status when ``True`` is active
                            ``False`` is inactive (bypass)
        """
        if status == self._active:
            return

        self._active = status
        self.observer.on_effect_status_toggled(self)

    def toggle(self):
        """
        Toggle the effect status: ``self.active = not self.active``
        """
        self.active = not self.active

    @property
    def connections(self):
        """
        :return list: Connections that this effects is present (with input or output port)
        """
        function = lambda connection: connection.input.effect == self \
                                   or connection.output.effect == self

        return tuple([c for c in self.patch.connections if function(c)])

    @property
    def json(self):
        """
        Get a json decodable representation of this effect

        :return dict: json representation
        """
        return self.__dict__

    @property
    @abstractmethod
    def __dict__(self):
        ...
