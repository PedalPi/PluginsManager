# PluginsManager

[![Build Status](https://travis-ci.org/PedalPi/PluginsManager.svg?branch=master)](https://travis-ci.org/PedalPi/PluginsManager) [![Documentation Status](https://readthedocs.org/projects/pedalpi-pluginsmanager/badge/?version=latest)](http://pedalpi-pluginsmanager.readthedocs.io/?badge=latest) [![Code Health](https://landscape.io/github/PedalPi/PluginsManager/master/landscape.svg?style=flat)](https://landscape.io/github/PedalPi/PluginsManager/master) [![codecov](https://codecov.io/gh/PedalPi/PluginsManager/branch/master/graph/badge.svg)](https://codecov.io/gh/PedalPi/PluginsManager)

Pythonic management of LV2 audio plugins with [mod-host](https://github.com/moddevices/mod-host).

**Documentation:**
   http://pedalpi-pluginsmanager.readthedocs.io/

**Code:**
   https://github.com/PedalPi/PluginsManager

**Python Package Index:**
   https://github.com/PedalPi/PluginsManager/tarball/master#egg=PedalPi-PluginsManager

**License:**
   Not yet

```python
manager = BanksManager()

bank = Bank('Bank 1')
manager.append(bank)

# All changes in bank are reproduced in modhost
mod_host = ModHost('localhost')
mod_host.connect()
manager.register(mod_host)

patch = Patch('Rocksmith')
bank.append(patch)

builder = Lv2EffectBuilder()
reverb = builder.build('http://calf.sourceforge.net/plugins/Reverb')
fuzz = builder.build('http://guitarix.sourceforge.net/plugins/gx_fuzzfacefm_#_fuzzfacefm_')
reverb2 = builder.build('http://calf.sourceforge.net/plugins/Reverb')

patch.append(reverb)
patch.append(fuzz)
patch.append(reverb2)

reverb.outputs[0].connect(fuzz.inputs[0])
reverb.outputs[1].connect(fuzz.inputs[0])
fuzz.outputs[0].connect(reverb2.inputs[0])
reverb.outputs[0].connect(reverb2.inputs[0])

fuzz.toggle()
fuzz.params[0].value = fuzz.params[0].minimum / fuzz.params[0].maximum

fuzz.outputs[0].disconnect(reverb2.inputs[0])
fuzz.toggle()

patch.effects.remove(fuzz)

for connection in list(patch.connections):
    patch.connections.remove(connection)

for effect in list(patch.effects):
    patch.effects.remove(effect)
```

## Test

```bash
coverage3 run --source=pluginsmanager setup.py test

coverage3 report
coverage3 html
firefox htmlcov/index.html
```

## Documentation

This project uses [Sphinx](http://www.sphinx-doc.org/) + [Read the Docs](readthedocs.org).

You can generate the documentation in your local machine: 

```bash
pip3 install sphinx

cd docs
make html

firefox buils/html/index.html
```
