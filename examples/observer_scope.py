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
from pluginsmanager.model.bank import Bank
from pluginsmanager.observer.updates_observer import UpdatesObserver


class MyAwesomeObserver(UpdatesObserver):

    def __init__(self, message):
        super(MyAwesomeObserver, self).__init__()
        self.message = message

    def on_bank_updated(self, bank, update_type, **kwargs):
        print(self.message)

    def on_pedalboard_updated(self, pedalboard, update_type, index, origin, **kwargs):
        pass

    def on_effect_status_toggled(self, effect, **kwargs):
        pass

    def on_effect_updated(self, effect, update_type, index, origin, **kwargs):
        pass

    def on_param_value_changed(self, param, **kwargs):
        pass

    def on_connection_updated(self, connection, update_type, pedalboard, **kwargs):
        pass

#############################
# Test

observer1 = MyAwesomeObserver("Hi! I am observer1")
observer2 = MyAwesomeObserver("Hi! I am observer2")
observer3 = MyAwesomeObserver("Hi! I am observer3")

manager = BanksManager()
manager.register(observer1)
manager.register(observer2)
manager.register(observer3)

#############################
print("Notify all observers")

bank = Bank('Bank 1')
manager.banks.append(bank)

print("Not notify observer 1")
with observer1:
    del manager.banks[0]

print("Not notify observer 2")
with observer2:
    manager.append(bank)

print("with inside a with not changes the behavior")
with observer1:
    manager.banks.remove(bank)
    with observer2:
        manager.append(bank)
