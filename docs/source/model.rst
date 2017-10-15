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

        Input->Port;
        Output->Port;

        MidiPort->Port;
        MidiInput->MidiPort;
        MidiOutput->MidiPort;

        Lv2Input->Input;
        Lv2Output->Output;
        Lv2MidiInput->MidiInput;
        Lv2MidiOutput->MidiOutput;

        SystemInput->Input;
        SystemOutput->Output;
        SystemMidiInput->MidiInput;
        SystemMidiOutput->MidiOutput;

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

.. .. inheritance-diagram::
    pluginsmanager.model.output.Output
    pluginsmanager.model.input.Input


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

Port
----

.. autoclass:: pluginsmanager.model.port.Port
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

MidiPort
--------

.. autoclass:: pluginsmanager.model.midi_port.MidiPort
   :members:
   :special-members:
   :exclude-members: __weakref__


MidiInput
---------

.. autoclass:: pluginsmanager.model.midi_input.MidiInput
   :members:
   :special-members:
   :exclude-members: __weakref__

MidiOutput
----------

.. autoclass:: pluginsmanager.model.midi_output.MidiOutput
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
