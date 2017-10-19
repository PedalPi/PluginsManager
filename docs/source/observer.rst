PedalPi - PluginsManager - Observers
====================================

An observer is a class that receives notifications of changes in model classes
(:class:`.Bank`, :class:`.Pedalboard`, :class:`.Effect`, :class:`.Param` ...).

Implementations
---------------

Some useful :class:`.UpdatesObserver` classes have been implemented. They are:

* :class:`.Autosaver`: Allows save the changes automatically in *json* data files.
* `ModHost <mod_host.html>`__: Allows use `mod-host`_,
  a LV2 host for Jack controllable via socket or command line

.. _mod-host: https://github.com/moddevices/mod-host

Using
-----

For use a observer, it's necessary register it in :class:`.BanksManager`::

    >>> saver = Autosaver()  # Autosaver is a UpdatesObserver
    >>> banks_manager = BanksManager()
    >>> banks_manager.register(saver)

For access all observers registered, use :attr:`.BanksManager.observers`::

    >>> saver in banks_manager.observers
    True

For remove a observer::

    >>> banks_manager.unregister(saver)

Creating a observer
-------------------

It is possible to create observers! Some ideas are:

 * Allow the use of other hosts (such as `Carla`_);
 * Automatically persist changes;
 * Automatically update a human-machine interface (such as LEDs and
   displays that inform the state of the effects).

For create a observer, is necessary create a class that extends
:class:`.UpdatesObserver`::

    class AwesomeObserver(UpdatesObserver):
       ...

:class:`.UpdatesObserver` contains a number of methods that must be
implemented in the created class. These methods will be called when changes occur::

    class AwesomeObserver(UpdatesObserver):

        def on_bank_updated(self, bank, update_type, index, origin, **kwargs):
            pass

        def on_pedalboard_updated(self, pedalboard, update_type, index, origin, **kwargs):
            pass

        def on_effect_status_toggled(self, effect, **kwargs):
            pass

        def on_effect_updated(self, effect, update_type, index, origin, **kwargs):
            pass

        def on_param_value_changed(self, param, **kwargs):
            pass

        def on_connection_updated(self, connection, update_type, pedalboard, **kwargs):
            pass


Use the ``update_type`` attribute to check what type of change occurred::

    class AwesomeObserver(UpdatesObserver):
        """Registers all pedalboards that have been deleted"""

        def __init__(self):
            super(AwesomeObserver, self).__init__()
            self.pedalboards_removed = []

        ...

        def on_pedalboard_updated(self, pedalboard, update_type, index, origin, **kwargs):
            if update_type == UpdateType.DELETED:
                self.pedalboards_removed.append(update_type)

        ...

.. _Carla: https://github.com/falkTX/Carla

Scope
-----

Notification problem
####################

There are cases where it makes no sense for an observer to be notified of a change.
Usually this occurs in interfaces for control, where through them actions can be
performed (activate an effect when pressing on a footswitch).
Control interfaces need to know of changes that occur so that their display
mechanisms are updated when some change occurs through another control interface.

Note that it does not make sense for an interface to be notified of the
occurrence of any change if it was the one that performed the action.

A classic example would be an interface for control containing footswitch and a led.
The footswitch changes the state of an effect and the led indicates whether it is
active or not. If another interface to control (a mobile application, for example)
changes the state of the effect to off, the led should reverse its state::

    class MyControllerObserver(UpdatesObserver):

        ...

        def on_effect_status_toggled(self, effect, **kwargs):
            # Using gpiozero
            # https://gpiozero.readthedocs.io/en/stable/recipes.html#led
            self.led.toggle()


However, in this situation, when the footswitch changes the effect state,
it is notified of the change itself. What can lead to inconsistency in the led::

    def pressed():
        effect.toggle()
        led.toggle()

    # footswitch is a button
    # https://gpiozero.readthedocs.io/en/stable/recipes.html#button
    footswitch.when_pressed = pressed



In this example, pressing the button:

1. ``pressed()`` is called;
2. The effect has its changed state (``effect.toggle()``);
3. ``on_effect_status_toggled(self, effect, ** kwargs)`` is called
   and the led is changed state (``self.led.toggle()``);
4. Finally, in ``pressed()`` is called ``led.toggle()``.

That is, ``led.toggle()`` will be **called twice instead of one**.

Scope solution
##############

Using ``with`` keyword, you can indicate which observer is performing the action,
allowing the observer not to be notified of the updates that occur in the ``with``
scope:

    >>> with observer1:
    >>>     del manager.banks[0]

Example
*******

.. note::

    The complete example can be obtained from the examples folder of the repository.
    `observer_scope.py`_

.. _examples folder in the repository: https://github.com/PedalPi/PluginsManager/tree/master/examples
.. _observer_scope.py: https://github.com/PedalPi/PluginsManager/blob/master/examples/observer_scope.py


Consider an Observer who only prints actions taken on a bank::

    class MyAwesomeObserver(UpdatesObserver):

        def __init__(self, message):
            super(MyAwesomeObserver, self).__init__()
            self.message = message

        def on_bank_updated(self, bank, update_type, **kwargs):
            print(self.message)

        ...


We will create two instances of this observer and perform some actions
to see how the notification will occur::

    >>> observer1 = MyAwesomeObserver("Hi! I am observer1")
    >>> observer2 = MyAwesomeObserver("Hi! I am observer2")

    >>> manager = BanksManager()
    >>> manager.register(observer1)
    >>> manager.register(observer1)


When notification occurs outside a ``with`` scope, all observers are informed
of the change::

    >>> bank = Bank('Bank 1')
    >>> manager.banks.append(bank)
    "Hi! I am observer1"
    "Hi! I am observer2"

We'll now limit the notification by telling you who performed the actions::

    >>> with observer1:
    >>> with observer1:
    ...     del manager.banks[0]
    "Hi! I am observer2"
    >>> with observer2:
    ...     manager.banks.append(bank)
    "Hi! I am observer1"


If there is ``with`` inside a ``with`` block, the behavior will not change,
ie it will not be cumulative

.. code-block:: python
   :linenos:
   :emphasize-lines: 2,4

    with observer1:
        manager.banks.remove(bank)
        with observer2:
            manager.banks.append(bank)


Line 2 will result in ``Hi! I am observer2`` and line 4 in ``Hi! I am observer1``

Base API
--------

UpdateType
##########

.. autoclass:: pluginsmanager.observer.update_type.UpdateType
   :members:
   :special-members:
   :exclude-members: __weakref__

UpdatesObserver
###############

.. autoclass:: pluginsmanager.observer.updates_observer.UpdatesObserver
   :members:
   :special-members:
   :exclude-members: __weakref__

pluginsmanager.observer.observable_list.ObservableList
######################################################

.. autoclass:: pluginsmanager.observer.observable_list.ObservableList
   :members:
   :special-members:
   :exclude-members: __weakref__

Implementations API
-------------------

pluginsmanager.observer.autosaver.autosaver.Autosaver
-----------------------------------------------------

.. autoclass:: pluginsmanager.observer.autosaver.autosaver.Autosaver
   :members:
   :special-members:
   :exclude-members: __weakref__
