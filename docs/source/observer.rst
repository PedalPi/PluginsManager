PedalPi - PluginsManager - Observers
====================================

Some useful :class:`.UpdatesObserver` classes have been implemented.

For register observers in :class:`.BanksManager`, use::

    >>> saver = Autosaver()
    >>> banks_manager = BanksManager()
    >>> banks_manager.register(saver)

For access all observers registered, use :attr:`.BanksManager.observers`::

    >>> saver in banks_manager.observers
    True

pluginsmanager.observer.autosaver.autosaver.Autosaver
-----------------------------------------------------

.. autoclass:: pluginsmanager.observer.autosaver.autosaver.Autosaver
   :members:
   :special-members:
   :exclude-members: __weakref__
