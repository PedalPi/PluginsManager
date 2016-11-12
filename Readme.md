# PluginsManager

[![Build Status](https://travis-ci.org/PedalPi/PluginsManager.svg?branch=master)](https://travis-ci.org/PedalPi/PluginsManager) [![Code Health](https://landscape.io/github/PedalPi/PluginsManager/master/landscape.svg?style=flat)](https://landscape.io/github/PedalPi/PluginsManager/master) [![codecov](https://codecov.io/gh/PedalPi/PluginsManager/branch/master/graph/badge.svg)](https://codecov.io/gh/PedalPi/PluginsManager)

Pythonic management of LV2 audio plugins with [mod-host](https://github.com/moddevices/mod-host).


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
coverage3 run --source=model,mod_host,model/lv2,util setup.py test

coverage3 report
coverage3 html
firefox htmlcov/index.html
```
