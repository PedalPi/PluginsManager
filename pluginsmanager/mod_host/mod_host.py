from pluginsmanager.model.updates_observer import UpdatesObserver
from pluginsmanager.model.update_type import UpdateType

from pluginsmanager.model.connection import Connection

from pluginsmanager.mod_host.host import Host


class ModHost(UpdatesObserver):
    TOKEN = 'ModHost'

    def __init__(self, address):
        self.token = ModHost.TOKEN
        self.address = address

        self.host = None
        self.patch = None

    def connect(self):
        """ Connect the object with mod-host """
        self.host = Host(self.address)

    def auto_connect(self):
        if self.patch is None or len(self.patch.effects) == 0:
            return

        first = self.patch.effects[0]
        last = self.patch.effects[-1]

        self.host.connect_input_in(first.inputs[0])

        before = first
        for effect in self.patch.effects[1:]:
            self.host.connect(Connection(before.outputs[0], effect.inputs[0]))
            before = effect

        self.host.connect_on_output(last.outputs[0], 1)
        self.host.connect_on_output(last.outputs[0], 2)

    def append(self, observer):
        self.observers.append(observer)

    ####################################
    # Observer
    ####################################
    def on_current_patch_change(self, patch, token=None):
        if self.patch is not None:
            for effect in self.patch.effects:
                self.on_effect_updated(effect, UpdateType.DELETED)

        self.patch = patch

        for effect in patch.effects:
            self.on_effect_updated(effect, UpdateType.CREATED)

    def on_bank_update(self, bank, update_type, token=None):
        pass

    def on_patch_updated(self, patch, update_type, token=None):
        self.on_current_patch_change(patch)

    def on_effect_updated(self, effect, update_type, token=None):
        if update_type == UpdateType.CREATED:
            self.host.add(effect)
            self._load_params_of(effect)
            self.on_effect_status_toggled(effect)

        if update_type == UpdateType.DELETED:
            self.host.remove(effect)

    def _load_params_of(self, effect):
        for param in effect.params:
            self.on_param_value_changed(param)

    def on_effect_status_toggled(self, effect, token=None):
        self.host.set_status(effect)

    def on_param_value_changed(self, param, token=None):
        self.host.set_param_value(param)

    def on_connection_updated(self, connection, update_type, token=None):
        if update_type == UpdateType.CREATED:
            self.host.connect(connection)
        elif update_type == UpdateType.DELETED:
            print('deleting', connection)
            self.host.disconnect(connection)
