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

.. image:: https://landscape.io/github/PedalPi/PluginsManager/master/landscape.svg?style=flat
    :target: https://landscape.io/github/PedalPi/PluginsManager/master
    :alt: Code Health


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

Example
-------

This examples uses `Calf`_ and `Guitarix`_ audio plugins

Download and install `mod-host`_. For more information, check the `ModHost section <mod_host.html>`__.

Start audio process

.. code-block:: bash

    # In this example, is starting a Zoom g3 series audio interface
    jackd -R -P70 -t2000 -dalsa -dhw:Series -p256 -n3 -r44100 -s &
    mod-host

Play!

.. code-block:: python

    from pluginsmanager.banks_manager import BanksManager
    from pluginsmanager.mod_host.mod_host import ModHost

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
    sys_effect = SystemEffectBuilder(client)

For manual input and output sound card definition, use:

.. code-block:: python

    sys_effect = SystemEffect('system', ['capture_1', 'capture_2'], ['playback_1', 'playback_2'])

.. note::

    **NOT ADD sys_effect** in any Pedalboard

Connecting *mode one*:

.. code-block:: python

    sys_effect.outputs[0].connect(reverb.inputs[0])

    reverb.outputs[0].connect(fuzz.inputs[0])
    reverb.outputs[1].connect(fuzz.inputs[0])
    fuzz.outputs[0].connect(reverb2.inputs[0])
    reverb.outputs[0].connect(reverb2.inputs[0])

    reverb2.outputs[0].connect(sys_effect.inputs[0])
    reverb2.outputs[0].connect(sys_effect.inputs[1])

Connecting *mode two*:

.. code-block:: python

    pedalboard.connections.append(Connection(sys_effect.outputs[0], reverb.inputs[0]))

    pedalboard.connections.append(Connection(reverb.outputs[0], fuzz.inputs[0]))
    pedalboard.connections.append(Connection(reverb.outputs[1], fuzz.inputs[0]))
    pedalboard.connections.append(Connection(fuzz.outputs[0], reverb2.inputs[0]))
    pedalboard.connections.append(Connection(reverb.outputs[0], reverb2.inputs[0]))

    pedalboard.connections.append(Connection(reverb2.outputs[0], sys_effect.inputs[0]))
    pedalboard.connections.append(Connection(reverb2.outputs[0], sys_effect.inputs[1]))

.. warning::

    If you need connect system_output with system_input directly (for a bypass, as example), only the
    second mode will works::

        pedalboard.connections.append(Connection(sys_effect.outputs[0], sys_effect.inputs[0]))

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
        pedalboard.connections.remove(connection)

    for effect in list(pedalboard.effects):
        pedalboard.effects.remove(effect)
    # or
    # for index in reversed(range(len(pedalboard.effects))):
        # del pedalboard.effects[index]

Maintenance
-----------

Test
****

It is not necessary for the mod_host process to be running

.. code-block:: bash

    coverage3 run --source=pluginsmanager setup.py test

    coverage3 report
    coverage3 html
    firefox htmlcov/index.html

Generate documentation
**********************

This project uses `Sphinx`_ + `Read the Docs`_.

You can generate the documentation in your local machine:

.. code-block:: bash

    pip3 install sphinx

    cd docs
    make html

    firefox build/html/index.html

.. _Sphinx: http://www.sphinx-doc.org/
.. _Read the Docs: http://readthedocs.org
.. _Calf: http://calf-studio-gear.org/
.. _Guitarix: http://guitarix.org/
