from abc import ABCMeta, abstractmethod

from unittest.mock import MagicMock


class Effect(metaclass=ABCMeta):
    """
    Representation of a audio plugin instance - LV2 plugin encapsulated as a jack client.

    Effect contains a `active` status (off=bypass), a list of :class:`Param`,
    a list of :class:`Input` and a list of :class:`Connection`
    """

    def __init__(self, patch=None):
        self.patch = patch
        self._active = True

        self._params = ()
        self._inputs = ()
        self._outputs = ()

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
    def params(self):
        """
        :return list[Param]: Params of effect
        """
        return self._params

    @property
    def inputs(self):
        """
        :return list[Input]: Inputs of effect
        """
        return self._inputs

    @property
    def outputs(self):
        """
        :return list[Output]: Outputs of effect
        """
        return self._outputs

    @property
    def active(self):
        """
        Effect status: active or bypass

        :getter: Current effect status
        :setter: Set the effect Status
        :type: bool
        """
        return self._active

    @active.setter
    def active(self, status):
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
        :return list[Connection]: Connections that this effects is present (with input or output port)
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
        pass
