from util.observable_list import ObservableList
from model.update_type import UpdateType

from unittest.mock import MagicMock


class Bank(object):
    """
    Bank is a data structure that contains :class:`Patch`. It's useful
    for group common patches, like "Patches will be used in
    the Sunday show"

    A fast bank overview::

    >>> bank = Bank('RHCP')
    >>> californication = Patch('Californication')

    >>> # Add patch in bank - mode A
    >>> bank.append(californication)
    >>> californication.bank == bank
    True

    >>> bank.patches[0] == californication
    True

    >>> # Add patch in bank - mode B
    >>> bank.patches.append(Patch('Dark Necessities'))
    >>> bank.patches[1].bank == bank
    True

    >>> # If you needs change patches order (swap), use pythonic mode
    >>> bank.patches[1], bank.patches[0] = bank.patches[0], bank.patches[1]
    >>> bank.patches[1] == californication
    True

    >>> # Set patch
    >>> bank.patches[0] = Patch('Can't Stop')
    >>> bank.patches[0].bank == bank
    True

    >>> del bank.patches[0]
    >>> bank.patches[0] == californication
    True

    You can also toggle patches into different banks::

    >>> bank1.patches[0], bank2.patches[2] = bank2.patches[0], bank1.patches[2]

    :param string name: Bank name
    """
    def __init__(self, name):
        self.index = -1
        self.name = name
        self.patches = ObservableList()
        self.patches.observer = self._patches_observer

        self.observer = MagicMock()

    def _patches_observer(self, update_type, patch, index):
        if update_type == UpdateType.CREATED \
        or update_type == UpdateType.UPDATED:
            patch.bank = self
            patch.observer = self.observer

        self.observer.on_patch_updated(patch, update_type)

        if update_type == UpdateType.DELETED:
            patch.bank = None
            patch.observer = MagicMock()

    @property
    def json(self):
        """
        Get a json decodable representation of this bank

        :return dict: json representation
        """
        return self.__dict__

    @property
    def __dict__(self):
        return {
            'index': self.index,
            'name': self.name,
            'patches': [patch.json for patch in self.patches]
        }

    def append(self, patch):
        """
        Add a :class:`Patch` in this bank

        This works same as::

        >>> bank.patches.append(patch)
        or::

        >>> bank.patches.insert(len(bank.patches), patch)

        :param Patch patch: Patch that will be added
        """
        self.patches.append(patch)
