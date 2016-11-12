from banks_manager import BanksManager
from mod_host.mod_host import ModHost

from model.bank import Bank
from model.patch import Patch

from model.lv2.lv2_effect_builder import Lv2EffectBuilder


if __name__ == "__main__":
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

    for connection in list(patch.connections):
        patch.connections.remove(connection)

    for effect in list(patch.effects):
        patch.effects.remove(effect)

    #mod_host.auto_connect()
