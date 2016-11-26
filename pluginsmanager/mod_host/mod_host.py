from pluginsmanager.model.updates_observer import UpdatesObserver
from pluginsmanager.model.update_type import UpdateType

from pluginsmanager.model.connection import Connection

from pluginsmanager.mod_host.host import Host


class ModHost(UpdatesObserver):
    """
    Python port for mod-host::
        `Mod-host`_ is a `LV2`_ host for Jack controllable via socket or command line.

    This class offers the mod-host control in a python API::

        # Create a mod-host, connect and register it in banks_manager
        mod_host = ModHost('localhost')
        mod_host.connect()
        banks_manager.register(mod_host)

        # Set the mod_host patch for a patch that the bank
        # has added in banks_manager
        mod_host.patch = my_awesome_patch

    The changes in current patch (``mod_host.patch``) will also result in mod-host::

        driver = my_awesome_patch.effects[0]
        driver.active = False

    .. note::

        For use, is necessary that the mod-host is running, for use, access

         * `Install dependencies`_
         * `Building mod-host`_
         * `Running mod-host`_

        For more JACK information, access `Demystifying JACK – A Beginners Guide to Getting Started with JACK`_

    **Example:**

        In this example, is starting a `Zoom G3`_ series audio interface. Others interfaces
        maybe needs others configurations.

    .. code-block:: bash

        # Starting jackdump process via console
        jackd -R -P70 -t2000 -dalsa -dhw:Series -p256 -n3 -r44100 -s &
        # Starting mod-host
        mod-host &

    :param string address: Computer mod-host process address (IP). If the
     process is running on the same computer that is running the python code
     uses `localhost`.

    .. _Mod-host: https://github.com/moddevices/mod-host
    .. _LV2: http://lv2plug.in
    .. _Install dependencies: https://github.com/deedos/mod-host/commit/0941d84fc48deb74e27cdcbf23a88db2007d5c6f
    .. _Zoom G3: https://www.zoom.co.jp/products/guitar/g3-guitar-effects-amp-simulator-pedal
    .. _Building mod-host: https://github.com/moddevices/mod-host#building
    .. _Running mod-host: https://github.com/moddevices/mod-host#running
    .. _Demystifying JACK – A Beginners Guide to Getting Started with JACK: http://libremusicproduction.com/articles/demystifying-jack-%E2%80%93-beginners-guide-getting-started-jack
    """

    TOKEN = 'ModHost'

    def __init__(self, address='localhost'):
        super(ModHost, self).__init__()
        self.token = ModHost.TOKEN
        self.address = address

        self.host = None
        self._patch = None

    def connect(self):
        """
        Connect the object with mod-host with the _address_ parameter informed in
        the initialization (``__init__(address)``)
        """
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

    @property
    def patch(self):
        """
        Currently managed patch (current patch)

        :getter: Current patch - Patch loaded by mod-host
        :setter: Set the patch that will be loaded by mod-host
        :type: Patch
        """
        return self._patch

    @patch.setter
    def patch(self, patch):
        self.on_current_patch_change(patch)

    ####################################
    # Observer
    ####################################
    def on_current_patch_change(self, patch, token=None):
        if self.patch is not None:
            for effect in self.patch.effects:
                self.on_effect_updated(effect, UpdateType.DELETED)

        self._patch = patch

        for effect in patch.effects:
            self.on_effect_updated(effect, UpdateType.CREATED)

    def on_bank_updated(self, bank, update_type, token=None, **kwargs):
        if self.patch is not None \
        and bank != self.patch.bank:
            return
        pass

    def on_patch_updated(self, patch, update_type, token=None, **kwargs):
        if patch != self.patch:
            return

        self.on_current_patch_change(patch)

    def on_effect_updated(self, effect, update_type, token=None, **kwargs):
        if effect.patch != self.patch:
            return

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
        if effect.patch != self.patch:
            return

        self.host.set_status(effect)

    def on_param_value_changed(self, param, token=None):
        if param.effect.patch != self.patch:
            return

        self.host.set_param_value(param)

    def on_connection_updated(self, connection, update_type, token=None):
        if connection.input.effect.patch != self.patch:
            return

        if update_type == UpdateType.CREATED:
            self.host.connect(connection)
        elif update_type == UpdateType.DELETED:
            self.host.disconnect(connection)
