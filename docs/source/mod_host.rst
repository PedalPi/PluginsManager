PedalPi - PluginsManager - ModHost
==================================

About `mod-host`
----------------

`mod-host`_ is a LV2 host for Jack controllable via socket or command line.
With it you can load audio plugins, connect, manage plugins.

For your use, is necessary download it

.. code-block:: bash

    git clone https://github.com/moddevices/mod-host
    cd mod-host
    make
    make install

Then boot the JACK process and start the `mod-host`.
Details about "JACK" can be found at https://help.ubuntu.com/community/What%20is%20JACK

.. code-block:: bash

    # In this example, is starting a Zoom g3 series audio interface
    jackd -R -P70 -t2000 -dalsa -dhw:Series -p256 -n3 -r44100 -s &
    mod-host

You can now connect to the mod-host through the Plugins Manager API.
Create a ModHost object with the address that is running the `mod-host` process.
Being in the same machine, it should be `'localhost'`

.. code-block:: python

    mod_host = ModHost('localhost')
    mod_host.connect()


Finally, register the mod-host in your BanksManager.
Changes made to the current pedalboard will be applied to `mod-host`

.. code-block:: python

    manager = BanksManager()
    # ...
    manager.register(mod_host)

To change the current pedalboard, change the `pedalboard` parameter to `mod_host`.
Remember that for changes to occur in `mod-host`, the `pedalboard` must belong to some `bank` of `banks_manager`.

.. code-block:: python

    mod_host.pedalboard = my_awesome_pedalboard

.. _mod-host: https://github.com/moddevices/mod-host

ModHost
-------
.. autoclass:: pluginsmanager.mod_host.mod_host.ModHost
   :members:
   :special-members:
   :exclude-members: __weakref__

ModHost internal
----------------

The classes below are for internal use of mod-host

Connection
**********
.. autoclass:: pluginsmanager.mod_host.connection.Connection
   :members:
   :special-members:
   :exclude-members: __weakref__

Host
****
.. autoclass:: pluginsmanager.mod_host.host.Host
   :members:
   :special-members:
   :exclude-members: __weakref__

ProtocolParser
**************
.. autoclass:: pluginsmanager.mod_host.protocol_parser.ProtocolParser
   :members:
   :special-members:
   :exclude-members: __weakref__
