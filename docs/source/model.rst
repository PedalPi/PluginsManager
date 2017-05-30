PedalPi - PluginsManager - Models
=================================

This page contains the model classes.

.. graphviz::

    digraph classes {
        graph [rankdir=BT];

        node [shape=rect, style=filled, color="#298029", fontname=Sans, fontcolor="#ffffff", fontsize=10];

        Pedalboard->Bank [
            dir="forward", arrowhead="odiamond", arrowtail="normal"
        ];
        Effect->Pedalboard [
            dir="forward", arrowhead="odiamond", arrowtail="normal"
        ];
        Param->Effect [
            dir="backward", arrowhead="diamond", arrowtail="normal"
        ];
        Connection->Pedalboard [
            dir="forward", arrowhead="odiamond", arrowtail="normal"
        ];
        Input->Effect [
            dir="backward", arrowhead="diamond", arrowtail="normal"
        ];
        Output->Effect [
           dir="backward", arrowhead="diamond", arrowtail="normal"
        ];

        Input->Connection [
            dir="backward", arrowhead="odiamond", arrowtail="normal"
        ];
        Output->Connection [
            dir="backward", arrowhead="odiamond", arrowtail="normal"
        ];
   }

.. graphviz::

   digraph classes {
       graph [rankdir=BT];
       node [shape=rect, style=filled, color="#298029", fontname=Sans, fontcolor="#ffffff", fontsize=10];

       Lv2Effect->Lv2Plugin[
           dir="backward", arrowhead="diamond", arrowtail="normal"
       ];
       Lv2Effect->Effect;
       SystemEffect->Effect;

       Lv2Input->Input;
       SystemInput->Input;

       Lv2Output->Output;
       SystemOutput->Output;

       Lv2Param->Param;
   }

.. graphviz::

    digraph classes {
        graph [rankdir=BT];
        node [shape=rect, style=filled, color="#298029", fontname=Sans, fontcolor="#ffffff", fontsize=10];

        Bank->BanksManager [dir="forward", arrowhead="odiamond", arrowtail="normal"];
        BanksManager->ObserverManager [dir="forward", arrowhead="none", arrowtail="normal"];
        UpdatesObserver->ObserverManager [dir="forward", arrowhead="odiamond", arrowtail="normal"];
        ModHost->UpdatesObserver
        AutoSaver->UpdatesObserver
    }

BanksManager
------------

.. autoclass:: pluginsmanager.banks_manager.BanksManager
   :members:
   :special-members:
   :exclude-members: __weakref__

Bank
----

.. autoclass:: pluginsmanager.model.bank.Bank
   :members:
   :special-members:
   :exclude-members: __weakref__

Connection
----------

.. autoclass:: pluginsmanager.model.connection.Connection
   :members:
   :special-members:
   :exclude-members: __weakref__

Effect
------

.. autoclass:: pluginsmanager.model.effect.Effect
   :members:
   :special-members:
   :exclude-members: __weakref__

Input
-----

.. autoclass:: pluginsmanager.model.input.Input
   :members:
   :special-members:
   :exclude-members: __weakref__

Output
------

.. autoclass:: pluginsmanager.model.output.Output
   :members:
   :special-members:
   :exclude-members: __weakref__

Param
-----

.. autoclass:: pluginsmanager.model.param.Param
   :members:
   :special-members:
   :exclude-members: __weakref__

Pedalboard
----------

.. autoclass:: pluginsmanager.model.pedalboard.Pedalboard
   :members:
   :special-members:
   :exclude-members: __weakref__

UpdateType
----------

.. autoclass:: pluginsmanager.model.update_type.UpdateType
   :members:
   :special-members:
   :exclude-members: __weakref__

UpdatesObserver
---------------

.. autoclass:: pluginsmanager.model.updates_observer.UpdatesObserver
   :members:
   :special-members:
   :exclude-members: __weakref__Z
