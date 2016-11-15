from pluginsmanager.banks_manager import BanksManager
from pluginsmanager.mod_host.mod_host import ModHost

from pluginsmanager.model.bank import Bank
from pluginsmanager.model.patch import Patch
from pluginsmanager.model.connection import Connection

from pluginsmanager.model.lv2.lv2_effect_builder import Lv2EffectBuilder

from pluginsmanager.model.system.system_effect import SystemEffect

if __name__ == "__main__":
#if True:
    sys_effect = SystemEffect('system', ('capture_1', 'capture_2'), ('playback_1', 'playback_2'))
    manager = BanksManager()

    bank = Bank('Bank 1')
    manager.append(bank)

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

    patch.connections.append(Connection(sys_effect.outputs[0], reverb.inputs[0]))
    patch.connections.append(Connection(reverb2.outputs[0], sys_effect.inputs[0]))

    for connection in list(patch.connections):
        patch.connections.remove(connection)

    for effect in list(patch.effects):
        patch.effects.remove(effect)

    #mod_host.auto_connect()
