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
   }


Bank
----

.. autoclass:: model.bank.Bank
   :members:
   :special-members:

Connection
----------

.. autoclass:: model.connection.Connection
   :members:
   :special-members:


Effect
------

.. autoclass:: model.effect.Effect
   :members:
   :special-members:

Input
-----

.. autoclass:: model.input.Input
   :members:
   :special-members:

Output
------

.. autoclass:: model.output.Output
   :members:
   :special-members:

Param
-----

.. autoclass:: model.param.Param
   :members:
   :special-members:

Patch
-----

.. autoclass:: model.patch.Patch
   :members:
   :special-members:

UpdateType
----------

.. autoclass:: model.update_type.UpdateType
   :members:
   :special-members:


UpdatesObserver
---------------

.. autoclass:: model.updates_observer.UpdatesObserver
   :members:
   :special-members:
