# Copyright 2017 SrMouraSilva
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from pluginsmanager.banks_manager import BanksManager
from pluginsmanager.observer.mod_host.mod_host import ModHost

from pluginsmanager.model.bank import Bank
from pluginsmanager.model.pedalboard import Pedalboard
from pluginsmanager.model.connection import Connection

from pluginsmanager.model.lv2.lv2_effect_builder import Lv2EffectBuilder

from pluginsmanager.model.system.system_effect import SystemEffect


if __name__ == '__main__':
    manager = BanksManager()

    bank = Bank('Bank 1')
    manager.append(bank)

    mod_host = ModHost('raspberrypi.local')
    mod_host.connect()
    manager.register(mod_host)

    pedalboard = Pedalboard('Rocksmith')
    bank.append(pedalboard)

    mod_host.pedalboard = pedalboard

    builder = Lv2EffectBuilder()

    reverb = builder.build('http://calf.sourceforge.net/plugins/Reverb')
    fuzz = builder.build('http://guitarix.sourceforge.net/plugins/gx_fuzz_#fuzz_')
    reverb2 = builder.build('http://calf.sourceforge.net/plugins/Reverb')

    pedalboard.append(reverb)
    pedalboard.append(fuzz)
    pedalboard.append(reverb2)

    sys_effect = SystemEffect('system', ['capture_1'], ['playback_1', 'playback_2'])

    pedalboard.connections.append(Connection(sys_effect.outputs[0], reverb.inputs[0]))

    reverb.outputs[0].connect(fuzz.inputs[0])
    reverb.outputs[1].connect(fuzz.inputs[0])
    fuzz.outputs[0].connect(reverb2.inputs[0])
    reverb.outputs[0].connect(reverb2.inputs[0])

    # Causes error
    reverb2.outputs[0].connect(sys_effect.inputs[0])
    reverb2.outputs[0].connect(sys_effect.inputs[1])
