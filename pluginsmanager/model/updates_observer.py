from abc import ABCMeta, abstractmethod


class UpdatesObserver(metaclass=ABCMeta):
    """
    The :class:`UpdatesObserver` is an abstract class definition for
    treatment of changes in some class model. Your methods are called
    when occurs any change in Bank, Pedalboard, Effect, etc.

    To do this, it is necessary that the :class:`UpdateObserver` objects
    be registered in some manager, so that it reports the changes. An
    example of a manager is :class:`BanksManager`.

    :class:`UpdateObserver` objects needs a Token, an *change identifier*:
    Some change managers can report changes that have occurred to observers
    who did not take action. This is useful for synchronizing views. Because
    the change-making information needs to be explicit, BanksManager does not
    implement this. As example, `Application`_ offers a manager with
    token support.

    .. _Application: https://github.com/PedalPi/Application
    """
    def __init__(self):
        self._token = None

    @property
    def token(self):
        """
        :getter: Observer token
        :setter: Set the token observer. A good place to do this is
                 in the constructor
        :type: string
        """
        return self._token

    @token.setter
    def token(self, token):
        self._token = token

    @abstractmethod
    def on_current_pedalboard_change(self, pedalboard, token=None):
        """
        Called when the current pedalboard changes

        :param Pedalboard pedalboard: New current pedalboard
        :param string token: Request token identifier
        """
        pass

    @abstractmethod
    def on_bank_updated(self, bank, update_type, token=None, **kwargs):
        """
        Called when changes occurs in any :class:`Bank`

        :param Bank bank: Bank changed.
        :param UpdateType update_type: Change type
        :param string token: Request token identifier
        :param int index: Bank index (or old index if update_type == UpdateType.DELETED)
        :param BanksManager origin: BanksManager that the bank is (or has) contained
        """
        pass

    @abstractmethod
    def on_pedalboard_updated(self, pedalboard, update_type, token=None, **kwargs):
        """
        Called when changes occurs in any :class:`Pedalboard`

        :param Pedalboard pedalboard: Pedalboard changed
        :param UpdateType update_type: Change type
        :param string token: Request token identifier
        :param int index: Pedalboard index (or old index if update_type == UpdateType.DELETED)
        :param Bank origin: Bank that the pedalboard is (or has) contained
        """
        pass

    @abstractmethod
    def on_effect_updated(self, effect, update_type, token=None, **kwargs):
        """
        Called when changes occurs in any :class:`Effect`

        :param Effect effect: Effect changed
        :param UpdateType update_type: Change type
        :param string token: Request token identifier
        :param int index: Effect index (or old index if update_type == UpdateType.DELETED)
        :param Pedalboard origin: Pedalboard that the effect is (or has) contained
        """
        pass

    @abstractmethod
    def on_effect_status_toggled(self, effect, token=None):
        """
        Called when any :class:`Effect` status is toggled

        :param Effect effect: Effect when status has been toggled
        :param string token: Request token identifier
        """
        pass

    @abstractmethod
    def on_param_value_changed(self, param, token=None):
        """
        Called when a param value change

        :param Param param: Param with value changed
        :param string token: Request token identifier
        """
        pass

    @abstractmethod
    def on_connection_updated(self, connection, update_type, token=None):
        """
        Called when changes occurs in any :class:`pluginsmanager.model.connection.Connection` of Pedalboard
        (adding, updating or removing connections)

        :param pluginsmanager.model.connection.Connection connection: Connection changed
        :param UpdateType update_type: Change type
        :param string token: Request token identifier
        """
        pass
