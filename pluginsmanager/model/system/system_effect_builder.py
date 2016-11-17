import jack

from pluginsmanager.model.system.system_effect import SystemEffect


class SystemEffectBuilder(object):
    """
    Automatic system physical ports dettection
    """
    def __init__(self, no_start_server=True):
        self.client = jack.Client("SystemEffectBuilder", no_start_server=no_start_server)

    def build(self):
        inputs = []
        outputs = []

        for port in self.client.get_ports(is_audio=True, is_physical=True):
            if port.is_input:
                inputs.append(port.shortname)
            else:
                outputs.append(port.shortname)

        return SystemEffect('system', tuple(outputs), tuple(inputs))
