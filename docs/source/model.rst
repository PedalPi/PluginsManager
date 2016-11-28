PedalPi - PluginsManager - Models
=================================

This page contains the model classes.

.. graphviz::

   digraph classes {
       graph [rankdir=TB];
       node [shape=rect, style=filled, color="#298029", fontname=Sans, fontcolor="#ffffff", fontsize=10];

       Bank->Patch [dir="forward", arrowhead="odiamond", arrowtail="normal"];
       Patch->Connection [dir="forward", arrowhead="odiamond", arrowtail="normal"];
       Patch->Effect [dir="forward", arrowhead="odiamond", arrowtail="normal"];
       Param->Effect [dir="backward", arrowhead="diamond", arrowtail="normal"];
       Input->Effect [dir="backward", arrowhead="diamond", arrowtail="normal"];
       Output->Effect [dir="backward", arrowhead="diamond", arrowtail="normal"];
   }

.. graphviz::

   digraph classes {
       graph [rankdir=TB];
       node [shape=rect, style=filled, color="#298029", fontname=Sans, fontcolor="#ffffff", fontsize=10];
       Lv2Effect->Effect;
       SystemEffect->Effect;

       Lv2Input->Input;
       SystemInput->Input;

       Lv2Output->Output;
       SystemOutput->Output;

       Lv2Param->Param;

       BanksManager->Bank [dir="forward", arrowhead="odiamond", arrowtail="normal"];
       BanksManager->ObserverManager [dir="forward", arrowhead="none", arrowtail="normal"];
       ObserverManager->UpdatesObserver [dir="forward", arrowhead="odiamond", arrowtail="normal"];
       ModHost->UpdatesObserver
   }


BanksManager
------------

.. autoclass:: pluginsmanager.banks_manager.BanksManager
   :members:
   :special-members:


Bank
----

.. autoclass:: pluginsmanager.model.bank.Bank
   :members:
   :special-members:

Connection
----------

.. autoclass:: pluginsmanager.model.connection.Connection
   :members:
   :special-members:


Effect
------

.. autoclass:: pluginsmanager.model.effect.Effect
   :members:
   :special-members:

Input
-----

.. autoclass:: pluginsmanager.model.input.Input
   :members:
   :special-members:

Output
------

.. autoclass:: pluginsmanager.model.output.Output
   :members:
   :special-members:

Param
-----

.. autoclass:: pluginsmanager.model.param.Param
   :members:
   :special-members:

Patch
-----

.. autoclass:: pluginsmanager.model.patch.Patch
   :members:
   :special-members:

UpdateType
----------

.. autoclass:: pluginsmanager.model.update_type.UpdateType
   :members:
   :special-members:


UpdatesObserver
---------------

.. autoclass:: pluginsmanager.model.updates_observer.UpdatesObserver
   :members:
   :special-members:
