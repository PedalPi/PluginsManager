PedalPi - PluginsManager
========================

.. image:: https://travis-ci.org/PedalPi/PluginsManager.svg?branch=master
    :target: https://travis-ci.org/PedalPi/PluginsManager
    :alt: Build Status

.. image:: https://readthedocs.org/projects/pedalpi-pluginsmanager/badge/?version=latest
    :target: http://pedalpi-pluginsmanager.readthedocs.io/?badge=latest
    :alt: Documentation Status

.. image:: https://codecov.io/gh/PedalPi/PluginsManager/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/PedalPi/PluginsManager
    :alt: Code coverage


Pythonic management of LV2 audio plugins with `mod-host`_.

.. _mod-host: https://github.com/moddevices/mod-host

**Documentation:**
   http://pedalpi-pluginsmanager.readthedocs.io/

**Code:**
   https://github.com/PedalPi/PluginsManager

**Python Package Index:**
   https://pypi.org/project/PedalPi-PluginsManager

**License:**
   `Apache License 2.0`_

.. _Apache License 2.0: https://github.com/PedalPi/PluginsManager/blob/master/LICENSE


Install
-------

Plugin Manager has dependencies that must be installed before installing the library.
Among the dependencies are `lv2ls`_ to check the installed audio plugins
and `PortAudio`_ for information on the audio interfaces through `PyAudio`_.

On Debian-based systems, run:


.. code-block:: bash

    sudo apt-get install -y portaudio19-dev python-all-dev lilv-utils --no-install-recommends

Of course, for PluginsManager to manage Lv2 audio plugins, it is necessary that they have installed
audio plugins to be managed. The `Guitarix`_ and `Calf Studio`_ projects provide some audio plugins.
To install them:

.. code-block:: bash

    pip install PedalPi-PluginsManager


.. _lv2ls: http://drobilla.net/man/lv2ls.1.html
.. _PortAudio: http://www.portaudio.com/
.. _PyAudio: https://people.csail.mit.edu/hubert/pyaudio/
.. _Calf Studio: http://calf-studio-gear.org/

Example
-------

.. note::

    Other examples are in the `examples folder in the repository`_.

.. _examples folder in the repository: https://github.com/PedalPi/PluginsManager/tree/master/examples

This examples uses `Calf`_ and `Guitarix`_ audio plugins.

Download and install `mod-host`_. For more information, check the `ModHost section <mod_host.html>`__.

Start audio process

.. code-block:: bash

    # In this example, is starting a Zoom g3 series audio interface
    jackd -R -P70 -t2000 -dalsa -dhw:Series -p256 -n3 -r44100 -s &
    mod-host

Play!

.. code-block:: python

    from pluginsmanager.banks_manager import BanksManager
    from pluginsmanager.observer.mod_host.mod_host import ModHost

    from pluginsmanager.model.bank import Bank
    from pluginsmanager.model.pedalboard import Pedalboard
    from pluginsmanager.model.connection import Connection

    from pluginsmanager.model.lv2.lv2_effect_builder import Lv2EffectBuilder

    from pluginsmanager.model.system.system_effect import SystemEffect

Creating a bank

.. code-block:: python

    # BanksManager manager the banks
    manager = BanksManager()

    bank = Bank('Bank 1')
    manager.append(bank)

Connecting with mod_host. Is necessary that the mod_host process already running

.. code-block:: python

    mod_host = ModHost('localhost')
    mod_host.connect()
    manager.register(mod_host)

Creating pedalboard

.. code-block:: python

    pedalboard = Pedalboard('Rocksmith')
    bank.append(pedalboard)
    # or
    # bank.pedalboards.append(pedalboard)

Loads pedalboard. All changes in pedalboard are reproduced in mod_host

.. code-block:: python

    mod_host.pedalboard = pedalboard

Add effects in the pedalboard

.. code-block:: python

    builder = Lv2EffectBuilder()

    reverb = builder.build('http://calf.sourceforge.net/plugins/Reverb')
    fuzz = builder.build('http://guitarix.sourceforge.net/plugins/gx_fuzz_#fuzz_')
    reverb2 = builder.build('http://calf.sourceforge.net/plugins/Reverb')

    pedalboard.append(reverb)
    pedalboard.append(fuzz)
    pedalboard.append(reverb2)
    # or
    # pedalboard.effects.append(reverb2)

For obtains automatically the sound card inputs and outputs, use `SystemEffectBuilder`.
It requires a `JackClient` instance, that uses `JACK-Client`_.

.. _JACK-Client: https://jackclient-python.readthedocs.io/

.. code-block:: python

    from pluginsmanager.jack.jack_client import JackClient
    client = JackClient()

    from pluginsmanager.model.system.system_effect_builder import SystemEffectBuilder
    sys_effect = SystemEffectBuilder(client).build()

For manual input and output sound card definition, use:

.. code-block:: python

    sys_effect = SystemEffect('system', ['capture_1', 'capture_2'], ['playback_1', 'playback_2'])

.. note::

    **NOT ADD sys_effect** in any Pedalboard

Connecting:

.. code-block:: python

    pedalbaord.connect(sys_effect.outputs[0], reverb.inputs[0])

    pedalbaord.connect(reverb.outputs[0], fuzz.inputs[0])
    pedalbaord.connect(reverb.outputs[1], fuzz.inputs[0])
    pedalbaord.connect(fuzz.outputs[0], reverb2.inputs[0])
    pedalbaord.connect(reverb.outputs[0], reverb2.inputs[0])

    pedalbaord.connect(reverb2.outputs[0], sys_effect.inputs[0])
    pedalbaord.connect(reverb2.outputs[0], sys_effect.inputs[1])

Connecting using ``ConnectionList``:

.. code-block:: python

    pedalboard.connections.append(Connection(sys_effect.outputs[0], reverb.inputs[0]))

    pedalboard.connections.append(Connection(reverb.outputs[0], fuzz.inputs[0]))
    pedalboard.connections.append(Connection(reverb.outputs[1], fuzz.inputs[0]))
    pedalboard.connections.append(Connection(fuzz.outputs[0], reverb2.inputs[0]))
    pedalboard.connections.append(Connection(reverb.outputs[0], reverb2.inputs[0]))

    pedalboard.connections.append(Connection(reverb2.outputs[0], sys_effect.inputs[0]))
    pedalboard.connections.append(Connection(reverb2.outputs[0], sys_effect.inputs[1]))

Set effect status (enable/disable bypass) and param value

.. code-block:: python

    fuzz.toggle()
    # or
    # fuzz.active = not fuzz.active

    fuzz.params[0].value = fuzz.params[0].minimum / fuzz.params[0].maximum

    fuzz.outputs[0].disconnect(reverb2.inputs[0])
    # or
    # pedalboard.connections.remove(Connection(fuzz.outputs[0], reverb2.inputs[0]))
    # or
    # index = pedalboard.connections.index(Connection(fuzz.outputs[0], reverb2.inputs[0]))
    # del pedalboard.connections[index]

    reverb.toggle()



Removing effects and connections:

.. code-block:: python

    pedalboard.effects.remove(fuzz)

    for connection in list(pedalboard.connections):
        pedalboard.disconnect(connection)
        # or
        #pedalboard.connections.remove(connection)

    for effect in list(pedalboard.effects):
        pedalboard.effects.remove(effect)
    # or
    # for index in reversed(range(len(pedalboard.effects))):
        # del pedalboard.effects[index]

Observer
--------

``ModHost`` is an **observer** (see ``UpdatesObserver``).
It is informed about all changes that
occur in some model instance (``BanksManager``, ``Bank``,
``Pedalboard``, ``Effect``, ``Param``, ...),
allowing it to communicate with the ``mod-host`` process transparently.

It is possible to create observers! Some ideas are:

 * Allow the use of other hosts (such as `Carla`_);
 * Automatically persist changes;
 * Automatically update a human-machine interface (such as LEDs and
   displays that inform the state of the effects).

How to implement and the list of Observers implemented by this
library can be accessed in the `Observer section <observer.html>`__.

.. _Carla: https://github.com/falkTX/Carla


Maintenance
-----------

Makefile
********

Execute ``make help`` for see the options

Generate documentation
**********************

This project uses `Sphinx`_ + `Read the Docs`_.

.. _Sphinx: http://www.sphinx-doc.org/
.. _Read the Docs: http://readthedocs.org
.. _Calf: http://calf-studio-gear.org/
.. _Guitarix: http://guitarix.org/
